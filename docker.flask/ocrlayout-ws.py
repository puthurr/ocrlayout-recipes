import io
import json

import flask
from flask import Flask, jsonify, request
from ocrlayout.bboxhelper import BBoxHelper, BBOXOCRResponse

app = Flask(__name__)

@app.route('/azureocr', methods=['POST'])
def azureocr():
    try:
        bboxresponse=BBoxHelper(verbose=False).processAzureOCRResponse(request.json)
    except Exception as ex:
        bboxresponse = {}
        bboxresponse["statuscode"]=500
        bboxresponse["exception"]=ex.__repr__()
        pass
    return json.dumps(bboxresponse.__dict__, default = lambda o: o.__dict__)

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=80)
