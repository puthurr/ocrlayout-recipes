# pip install spacy
# python -m spacy download en_core_web_sm
import spacy
from spacy import displacy

import os
from pathlib import Path
import json
try:
    from inspect import getfullargspec as get_arg_spec
except ImportError:
    from inspect import getargspec as get_arg_spec
import os
import sys
import types

# Azure CV Support
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from ocrlayout.bboxhelper import BBOXOCRResponse,BBoxHelper

IMAGES_FOLDER = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), "./images")

RESULTS_FOLDER = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), "./tests-results")

def iterate_all_images(ocrengines=[],filter=None,callOCR=True,verbose=False):
    """OCR Text detection for all images 
    Iterate through all images located in the IMAGES_FOLDER and call all OCR Engines
    """
    for filename in os.listdir(IMAGES_FOLDER):
        if filter:
            if filter not in filename:
                continue
        if '.DS_Store' in filename:
            continue
        for engine in ocrengines:
            (orig,new) = engine(os.path.join(IMAGES_FOLDER, filename),callOCR,verbose)
            doc1=spacy_me(filename,orig,"ORIG")
            doc2=spacy_me(filename,new,"NEW")
            displacy.serve([doc1,doc2], style="ent")

def azure_batch_read_file_in_stream(filename=None,callOCR=True,verbose=False):
    """RecognizeTextUsingBatchReadAPI.
    This will recognize text of the given image using the Batch Read API.
    """
    import time
    #
    # Azure Specific
    #
    SUBSCRIPTION_KEY_ENV_NAME = os.environ.get("COMPUTERVISION_SUBSCRIPTION_KEY", None)
    COMPUTERVISION_LOCATION = os.environ.get("COMPUTERVISION_LOCATION", "westeurope")

    azure_client = ComputerVisionClient(
        endpoint="https://" + COMPUTERVISION_LOCATION + ".api.cognitive.microsoft.com/",
        credentials=CognitiveServicesCredentials(SUBSCRIPTION_KEY_ENV_NAME)
    )
    print("AZURE Image Name {}".format(filename))
    p = Path(filename)
    (imgname,imgext) = os.path.splitext(p.name)

    # Check if we have a cached ocr response already for this provider
    invokeOCR=callOCR
    if not callOCR:
        if not os.path.exists(os.path.join(RESULTS_FOLDER, imgname+".azure.read.json")):
            invokeOCR=True

    if invokeOCR:
        # Azure Computer Vision Call
        with open(os.path.join(IMAGES_FOLDER, filename), "rb") as image_stream:
            job = azure_client.read_in_stream(
                image=image_stream,
                raw=True
            )
        operation_id = job.headers['Operation-Location'].split('/')[-1]

        image_analysis = azure_client.get_read_result(operation_id,raw=True)
        while image_analysis.output.status in ['notstarted', 'running']:
            time.sleep(1)
            image_analysis = azure_client.get_read_result(operation_id=operation_id,raw=True)
        print("\tJob completion is: {}".format(image_analysis.output.status))
        print("\tRecognized {} page(s)".format(len(image_analysis.output.analyze_result.read_results)))

        with open(os.path.join(RESULTS_FOLDER, imgname+".azure.read.json"), 'w') as outfile:
            outfile.write(image_analysis.response.content.decode("utf-8"))
        ocrresponse=image_analysis.response.content.decode("utf-8")
    else: 
        # Use local OCR cached response when available
        with open(os.path.join(RESULTS_FOLDER, imgname+".azure.read.json"), 'r') as cachefile:
            ocrresponse = cachefile.read().replace('\n', '')

    # Convert the original ocrresponse into proper object
    ocrresponse=BBOXOCRResponse.from_azure(json.loads(ocrresponse))
    # load the original
    original_text=""
    for page in ocrresponse.pages:
        for line in page.Lines:
            original_text+=(line.Text)
            original_text+=('\n')

    # Create BBOX OCR Response from Azure CV string response
    bboxresponse=BBoxHelper(verbose=verbose).processAzureOCRResponse(ocrresponse,boxSeparator=["","\r\n"])

    return (original_text,bboxresponse.Text)

def spacy_me(filename,text,tag):
    # Load English tokenizer, tagger, parser, NER and word vectors
    nlp = spacy.load("en_core_web_sm")

    doc = nlp(text)
    # Analyze syntax
    print(tag+"|Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
    print(tag+"|Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])

    # Find named entities, phrases and concepts
    entities=[]
    for entity in doc.ents:
        entities.append(entity.text+" "+entity.label_)
    with open(os.path.join(RESULTS_FOLDER, filename+"."+tag+".spacy.named_entities.json"), 'w') as outfile:
        outfile.write("\n".join(sorted(entities)))
    # Extract the sentences...
    sentences=[]
    for sent in doc.sents:
        sentences.append(sent.text)
    with open(os.path.join(RESULTS_FOLDER, filename+"."+tag+".spacy.sentences.json"), 'w') as outfile:
        outfile.write("\n".join(sentences))

    doc.user_data["title"] = (filename+"."+tag)
    return doc

if __name__ == "__main__":
    import sys, os.path
    sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..", "..")))
    import os
    import argparse
    parser = argparse.ArgumentParser(description='Call OCR outputs for a given image or images dir')
    parser.add_argument('--image',type=str,required=False,help='Process a single image',default=None)
    parser.add_argument('--imagesdir',type=str,required=False,help='Process all images contained in the given directory',default=IMAGES_FOLDER)
    parser.add_argument('--filter',type=str,required=False,help='Filter the images to process based on their filename',default="")
    parser.add_argument('--outputdir',type=str,required=False,help='Define where all outputs will be stored',default=RESULTS_FOLDER)
    parser.add_argument('--callocr', dest='callocr', action='store_true',help='flag to invoke online OCR Service')
    parser.set_defaults(callocr=False)
    parser.add_argument('-v','--verbose', dest='verbose', action='store_true',help='DEBUG logging level')
    parser.set_defaults(verbose=False)
    args = parser.parse_args()

    # Output dir
    if args.outputdir:
        RESULTS_FOLDER=args.outputdir

    if not os.path.exists(RESULTS_FOLDER):
        os.makedirs(RESULTS_FOLDER)

    # Check for available OCR engine functions
    ocrengines=[]
    for func in list(globals().values()):
        if not isinstance(func, types.FunctionType):
            continue
        arguments = get_arg_spec(func).args
        if 'filename' in arguments:
            ocrengines.append(func)

    if len(ocrengines)==0:
        print("No OCR Engine found. exiting.")
        exit

    # Process a single image
    if args.image:
        if not os.path.exists(args.image):
            print("Image path doesn't exist.")
            exit
        else:
            for engine in ocrengines:
                (orig,new) = engine(filename=args.image,callOCR=args.callocr,verbose=args.verbose)
                spacy_me(orig,"ORGI")
                spacy_me(new,"NEW")
    else:
        if args.imagesdir:
            if not os.path.exists(args.imagesdir):
                print("Images folder doesn't exist.")
                exit
            else: 
                IMAGES_FOLDER=args.imagesdir
        # Process all images contained the IMAGES_FOLDER
        iterate_all_images(ocrengines=ocrengines,filter=args.filter,callOCR=args.callocr,verbose=args.verbose)
        