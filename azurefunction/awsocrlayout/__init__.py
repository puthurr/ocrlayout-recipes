import logging
import json
import azure.functions as func
from ocrlayout.bboxhelper import BBoxHelper

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    bboxresponse={}
    try:
        width = req.params.get('width')
        if not width:
            return func.HttpResponse(body=f'Missign width parameter',status_code=400)

        height = req.params.get('height')
        if not height:
            return func.HttpResponse(body=f'Missign height parameter',status_code=400)

        req_body = req.get_json()
        if len(req_body)==0:
            return func.HttpResponse(body=f'Empty request body',status_code=400)

        bboxresponse=BBoxHelper(verbose=False).processAWSOCRResponse(req_body,width=int(width),height=int(height))

    except Exception as ex:
        bboxresponse["statuscode"]=500
        bboxresponse["exception"]=ex.__repr__()

    if hasattr(bboxresponse,'__dict__'):
        return func.HttpResponse(json.dumps(bboxresponse.__dict__, default = lambda o: o.__dict__))
    else:
        return func.HttpResponse(json.dumps(bboxresponse))