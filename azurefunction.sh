# Azure Functions:
#         azureocrlayout: [POST] http://localhost:7071/api/azureocrlayout
#         awsocrlayout: [GET,POST] http://localhost:7071/api/awsocrlayout
#         googleocrlayout: [POST] http://localhost:7071/api/googleocrlayout

# Images for testing

# image253.aws.textextract.json
# image253.google.vision.json	
# image253.azure.read.json	

# scan3.azure.read.json
# scan3.aws.textextract.json	
# scan3.google.vision.json

# AZURE 
curl -H "Content-Type: application/json" --data @ocr_jsons/scan3.azure.read.json http://localhost:7071/api/azureocrlayout
curl -H "Content-Type: application/json" --data @ocr_jsons/image253.azure.read.json http://localhost:7071/api/azureocrlayout
# GOOGLE
curl -H "Content-Type: application/json" --data @ocr_jsons/scan3.google.vision.json http://localhost:7071/api/googleocrlayout
curl -H "Content-Type: application/json" --data @ocr_jsons/image253.google.vision.json http://localhost:7071/api/googleocrlayout
# AWS
curl -H "Content-Type: application/json" --data @ocr_jsons/scan3.aws.textextract.json "http://localhost:7071/api/awsocrlayout?width=674&height=1015"
curl -H "Content-Type: application/json" --data @ocr_jsons/image253.aws.textextract.json "http://localhost:7071/api/awsocrlayout?width=577&height=443"
