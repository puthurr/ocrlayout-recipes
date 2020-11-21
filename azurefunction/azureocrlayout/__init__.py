import logging
import json
import azure.functions as func
from ocrlayout.bboxhelper import BBoxHelper

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    bboxresponse={}
    try:
        req_body = req.get_json()
        if len(req_body)==0:
            return func.HttpResponse(body=f'Empty request body',status_code=400)
        bboxresponse=BBoxHelper(verbose=False).processAzureOCRResponse(req_body)
    except Exception as ex:
        bboxresponse["statuscode"]=500
        bboxresponse["exception"]=ex.__repr__()

    if hasattr(bboxresponse,'__dict__'):
        return func.HttpResponse(json.dumps(bboxresponse.__dict__, default = lambda o: o.__dict__))
    else:
        return func.HttpResponse(json.dumps(bboxresponse))