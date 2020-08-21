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
        print(type(request.data))
        print(type(request.json))
        # bboxresponse=BBoxHelper(verbose=True).processAzureOCRResponse(str(request.data))
        bboxresponse=BBoxHelper(verbose=True).processAzureOCRResponse(request.json)
        print(bboxresponse.text)
    except Exception as ex:
        bboxresponse = {}
        bboxresponse["statuscode"]=500
        bboxresponse["exception"]=ex.__repr__()

    # return json.dumps(bboxresponse)
    return json.dumps(bboxresponse.__dict__, default = lambda o: o.__dict__)
        # 
        # return jsonify(bboxresponse)

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=80)
