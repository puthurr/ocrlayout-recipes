# pip install spacy
# python -m spacy download en_core_web_sm
import json
import os
import sys
import types
from pathlib import Path

# Azure CV Support
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

from ocrlayout.bboxhelper import BBoxHelper, BBOXOCRResponse

try:
    from inspect import getfullargspec as get_arg_spec
except ImportError:
    from inspect import getargspec as get_arg_spec

# spaCy
import spacy
from spacy import displacy

# Speech SDK
import azure.cognitiveservices.speech as speechsdk
# Copied from 
# https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/f356a22eda60717aec95f1a9becf6f5bbfbf8aca/samples/python/console/speech_synthesis_sample.py
#
speech_key = os.environ.get("COMPUTERVISION_SUBSCRIPTION_KEY", None)
service_region = os.environ.get("COMPUTERVISION_LOCATION", "westeurope")

IMAGES_FOLDER = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), "./images")

RESULTS_FOLDER = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), "./tests-results")

def process_all_images(ocrengines=[],filter=None,callOCR=True,verbose=False,spacy=True,voice=True):
    """OCR Text detection for all images 
    Iterate through all images located in the IMAGES_FOLDER and call all OCR Engines
    """
    for filename in os.listdir(IMAGES_FOLDER):
        if filter:
            if filter not in filename:
                continue
        if '.DS_Store' in filename:
            continue
        process_one_image(os.path.join(IMAGES_FOLDER, filename),ocrengines,callOCR,verbose,spacy,voice)

def process_one_image(full_path_name,ocrengines=[],callOCR=True,verbose=False,spacy=True,voice=True):
    print("Input File Name {}".format(full_path_name))
    p = Path(full_path_name)
    (imgname,imgext) = os.path.splitext(p.name)

    # OCR
    for engine in ocrengines:
        (original_text,new_text) = engine(full_path_name,callOCR,verbose)

        if spacy:       
            sentences = spacy_processing(imgname,original_text,new_text)

        if voice:
            if spacy:
                voice_processing(imgname,sentences)
            else:
                voice_processing(imgname,new_text.replace('\n', ''))
#
# Text To Speech
#
def voice_processing(imgname,text):
    print("VOICE PROCESSING")
    if "de_" in imgname:
        speech_synthesis_with_language(imgname,text,language="de-DE",voice="de-DE-KatjaNeural")
    elif "en_" in imgname:
        speech_synthesis_with_language(imgname,text,language="en-US",voice="en-AU-NatashaNeural")

def speech_synthesis_with_language(input_doc_name,input_doc,language,voice):
    """performs speech synthesis to the default speaker with specified spoken language"""
    # Creates an instance of a speech config with specified subscription key and service region.
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    # Sets the synthesis language.
    # The full list of supported languages can be found here:
    # https://docs.microsoft.com/azure/cognitive-services/speech-service/language-support#text-to-speech
    speech_config.speech_synthesis_language = language

    if voice:
        speech_config.speech_synthesis_voice_name = voice

    # Sets the synthesis output format.
    # The full list of supported format can be found here:
    # https://docs.microsoft.com/azure/cognitive-services/speech-service/rest-text-to-speech#audio-outputs
    speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3)

    # Creates a speech synthesizer using file as audio output.
    # Replace with your own audio file name.
    file_name = os.path.join(RESULTS_FOLDER,input_doc_name+"."+language+".mp3")
    file_config = speechsdk.audio.AudioOutputConfig(filename=file_name)

    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=file_config)

    # Get the text from ocrlayout output 
    result = speech_synthesizer.speak_text_async(input_doc).get()
    # Check result
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized to speaker for text [{}] with language [{}]".format(input_doc, language))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))

#
# spaCy : Entities, Sentences (english and German only)
# 
def spacy_processing(imgname,orig,new):
    print("SPACY PROCESSING")

    (doc1,_)=spacy_me(imgname,orig,"before")
    html1 = displacy.render(doc1,style="ent",page=True)
    with open(os.path.join(RESULTS_FOLDER, imgname+".before.spacy.entities.html"), 'w') as outfile:
        outfile.write(html1)

    (doc2,sentences)=spacy_me(imgname,new,"after")
    html2 = displacy.render(doc2,style="ent",page=True)
    with open(os.path.join(RESULTS_FOLDER, imgname+".after.spacy.entities.html"), 'w') as outfile:
        outfile.write(html2)

    return sentences

def spacy_me(input_doc_name,input_doc,log_prefix):

    if "en_" in input_doc_name:
        # Load English tokenizer, log_prefixger, parser, NER and word vectors
        nlp = spacy.load("en_core_web_sm")
    elif "de_" in input_doc_name:
        nlp = spacy.load("de_core_news_sm")

    doc = nlp(input_doc)
    # Analyze syntax
    print(log_prefix+"|Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
    print(log_prefix+"|Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])

    # Find named entities, phrases and concepts
    entities=[]
    for entity in doc.ents:
        entities.append(entity.text+" "+entity.label_)
    with open(os.path.join(RESULTS_FOLDER, input_doc_name+"."+log_prefix+".spacy.named_entities.json"), 'w') as outfile:
        outfile.write("\n".join(sorted(entities)))
    # Extract the sentences...
    sentences=[]
    for sent in doc.sents:
        sentences.append(sent.text)
    with open(os.path.join(RESULTS_FOLDER, input_doc_name+"."+log_prefix+".spacy.sentences.json"), 'w') as outfile:
        outfile.write("\n".join(sentences))

    doc.user_data["title"] = (input_doc_name+"."+log_prefix)

    return (doc,"\n".join(sentences))

#
# OCR
#
def azure_batch_read_in_stream(filename=None,callOCR=True,verbose=False):
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
        # with open(os.path.join(IMAGES_FOLDER, filename), "rb") as image_stream:
        with open(filename, "rb") as image_stream:
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

    # load the original response to get the text as-is
    original_text=""
    for page in ocrresponse.pages:
        for line in page.lines:
            original_text+=(line.text)
            original_text+=('\n')

    with open(os.path.join(RESULTS_FOLDER, imgname+".before.azure.read.txt"), 'w') as outfile:
        outfile.write(original_text)

    # Create BBOX OCR Response from Azure CV string response
    bboxresponse=BBoxHelper(verbose=verbose).processAzureOCRResponse(ocrresponse)
    with open(os.path.join(RESULTS_FOLDER, imgname+".azure.bbox.json"), 'w') as outfile:
        outfile.write(json.dumps(bboxresponse.__dict__, default = lambda o: o.__dict__, indent=4))

    with open(os.path.join(RESULTS_FOLDER, imgname+".after.azure.read.txt"), 'w') as outfile:
        outfile.write(bboxresponse.text)

    return (original_text,bboxresponse.text)

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
    parser.add_argument('--spacy', dest='spacy', action='store_true',help='Enable spaCy processing',default=False)
    parser.add_argument('--voice', dest='voice', action='store_true',help='Enable Voice processing',default=False)
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
            process_one_image(args.image,ocrengines,args.callocr,args.verbose,args.spacy,args.voice)
    else:
        if args.imagesdir:
            if not os.path.exists(args.imagesdir):
                print("Images folder doesn't exist.")
                exit
            else: 
                IMAGES_FOLDER=args.imagesdir

        # Process all images contained the IMAGES_FOLDER
        process_all_images(ocrengines=ocrengines,filter=args.filter,callOCR=args.callocr,verbose=args.verbose)
