# 
# Usage
#    python recipel_simple.py --document <path_to_doc> 
#
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

RESULTS_FOLDER = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), "./tests-results")

def process_one_image(full_path_name,ocrengines=[],callOCR=True,verbose=False,spacy=False,voice=False):
    print("Input File Name {}".format(full_path_name))
    p = Path(full_path_name)
    (imgname,imgext) = os.path.splitext(p.name)
    # OCR
    for engine in ocrengines:
        (original_text,new_text) = engine(full_path_name,callOCR,verbose)

#
# Azure Specific
#
SUBSCRIPTION_KEY_ENV_NAME = os.environ.get("COMPUTERVISION_SUBSCRIPTION_KEY", None)
COMPUTERVISION_LOCATION = os.environ.get("COMPUTERVISION_LOCATION", "westeurope")

azure_client = ComputerVisionClient(
    endpoint="https://" + COMPUTERVISION_LOCATION + ".api.cognitive.microsoft.com/",
    credentials=CognitiveServicesCredentials(SUBSCRIPTION_KEY_ENV_NAME)
)
#
# OCR
#
def azure_batch_read_in_stream(filename=None,callOCR=True,verbose=False):
    """RecognizeTextUsingBatchReadAPI.
    This will recognize text of the given image using the Batch Read API.
    """
    import time
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

        with open(os.path.join(RESULTS_FOLDER, imgname+".azure.read.json"), 'w',encoding='utf8') as outfile:
            outfile.write(image_analysis.response.content.decode("utf-8"))
        ocrresponse=image_analysis.response.content.decode("utf-8")
    else: 
        # Use local OCR cached response when available
        with open(os.path.join(RESULTS_FOLDER, imgname+".azure.read.json"), 'r',encoding='utf8') as cachefile:
            ocrresponse = cachefile.read().replace('\n', '')

    # Convert the original ocrresponse into proper object
    ocrresponse=BBOXOCRResponse.from_azure(json.loads(ocrresponse))

    # load the original response to get the text as-is
    original_text=""
    for page in ocrresponse.pages:
        for line in page.lines:
            original_text+=(line.text)
            original_text+=('\n')

    with open(os.path.join(RESULTS_FOLDER, imgname+".before.azure.read.txt"), 'w',encoding='utf8') as outfile:
        outfile.write(original_text)

    # Create BBOX OCR Response from Azure CV string response
    bboxresponse=BBoxHelper(verbose=verbose,customcfgfilepath='./myconfig.json').processAzureOCRResponse(ocrresponse)
    with open(os.path.join(RESULTS_FOLDER, imgname+".azure.bbox.json"), 'w',encoding='utf8') as outfile:
        outfile.write(json.dumps(bboxresponse.__dict__, default = lambda o: o.__dict__, indent=4))

    with open(os.path.join(RESULTS_FOLDER, imgname+".after.azure.read.txt"), 'w',encoding='utf8') as outfile:
        outfile.write(bboxresponse.text)

    return (original_text,bboxresponse.text)

if __name__ == "__main__":
    import sys, os.path
    sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..", "..")))
    import os
    import argparse
    parser = argparse.ArgumentParser(description='Call OCR outputs for a given document')
    parser.add_argument('--document',type=str,required=False,help='Process a single image',default=None)
    parser.add_argument('--outputdir',type=str,required=False,help='Define where all outputs will be stored',default=RESULTS_FOLDER)
    parser.add_argument('-v','--verbose', dest='verbose', action='store_true',help='DEBUG logging level')
    parser.set_defaults(verbose=False)
    args = parser.parse_args()

    callocr=True
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
        print("No OCR Engine found. bye.")
        exit

    # Process a single image
    if args.document:
        if not os.path.exists(args.document):
            print("Image path doesn't exist.")
            exit
        else:
            process_one_image(args.document,ocrengines,callocr,args.verbose)
    else:
        print("Please provide a document path. bye.")

