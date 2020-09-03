import io
import json
import flask
from flask import Flask, jsonify, request

from ocrlayout.bboxhelper import BBoxHelper, BBOXOCRResponse

app = Flask(__name__)

@app.route('/azureocr', methods=['POST'])
def azureocr():
    bboxresponse={}
    try:
        bboxresponse=BBoxHelper(verbose=True).processAzureOCRResponse(request.json)
    except Exception as ex:
        bboxresponse = {}
        bboxresponse["statuscode"]=500
        bboxresponse["exception"]=ex.__repr__()

    if hasattr(bboxresponse,'__dict__'):
        return json.dumps(bboxresponse.__dict__, default = lambda o: o.__dict__)
    else:
        return bboxresponse

@app.route('/googleocr', methods=['POST'])
def googleocr():
    bboxresponse={}
    try:
        bboxresponse=BBoxHelper(verbose=True).processGoogleOCRResponse(request.json)
    except Exception as ex:
        bboxresponse = {}
        bboxresponse["statuscode"]=500
        bboxresponse["exception"]=ex.__repr__()

    if hasattr(bboxresponse,'__dict__'):
        return json.dumps(bboxresponse.__dict__, default = lambda o: o.__dict__)
    else:
        return bboxresponse

@app.route('/awsocr', methods=['POST'])
def awsocr():
    bboxresponse={}
    try:
        width = int(request.args.get('width'))
        height = int(request.args.get('height'))
        bboxresponse=BBoxHelper(verbose=True).processAWSOCRResponse(request.json,width,height)
    except Exception as ex:
        bboxresponse = {}
        bboxresponse["statuscode"]=500
        bboxresponse["exception"]=ex.__repr__()

    print(bboxresponse)

    if hasattr(bboxresponse,'__dict__'):
        return json.dumps(bboxresponse.__dict__, default = lambda o: o.__dict__)
    else:
        return bboxresponse

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=80)
