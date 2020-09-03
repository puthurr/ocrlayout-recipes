# OCRLayout standalone container service built using Docker, Python and Flask 

>This documentation is adapted from the work of the (Azure Cognitive Search Team)[https://github.com/Azure-Samples/azure-search-knowledge-mining/tree/master/03%20-%20Data%20Science%20and%20Custom%20Skills/Docker%20Flask%20Skill]

Since this is hosted in a Docker container, the service can be easily scaled using Kubernetes.  This readme will walk through how to setup and configure the docker instance to run ocrlayout as a service.

## Getting Started

The first thing you will want to do is to build the Docker container.  To do this, you will need:

* [Docker Desktop](https://www.docker.com/products/docker-desktop) installed 
* [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)
* An Azure subscription where we will be hosting the docker container
* The files from this Github directory downloaded locally

## Build the Docker Image

From your desktop favorite Terminal and go to the directory you downloaded the Github files, of which you should have: 
* ocrlayout-ws.py: Hosting the python code which is run as a Flask service.  
* requirements.txt: Includes all the python packages used
* DockerFile: Details on how to build the docker image

Type: <code>docker.exe build -t ocrlayout .</code>

Note, this might take a while as there is a lot to download

## Run the Docker Container Locally

Next, we will test the image locally to make sure it works as expected.  Assuming you have nothing else running on port 5000, you can start the container:

Type: <code>docker.exe run -p 5005:80 ocrlayout</code>

## Test the Docker Container Locally

There are a lot of tools for testing APis, such as [Postman](https://www.getpostman.com/), or CURL.  Here is an example of a request to test the container:

POST: http://localhost:5005/azureocr

Header: 
<code>Content-Type: application/json</code>

Body (raw): 

```json
{"status":"succeeded","createdDateTime":"2020-07-29T17:12:34Z","lastUpdatedDateTime":"2020-07-29T17:12:34Z","analyzeResult":{"version":"3.0.0","readResults":[{"page":1,"language":"en","angle":0,"width":577,"height":443,"unit":"pixel","lines":[{"boundingBox":[498,73,563,73,563,84,498,83],"text":"Fossil evidence","words":[{"boundingBox":[498,74,521,74,521,84,498,84],"text":"Fossil","confidence":0.976},{"boundingBox":[523,74,564,74,563,84,523,84],"text":"evidence","confidence":0.981}]},{"boundingBox":[190,84,236,84,236,97,190,97],"text":"AFRICA","words":[{"boundingBox":[191,85,236,85,236,97,191,97],"text":"AFRICA","confidence":0.983}]},{"boundingBox":[498,86,558,85,559,96,498,96],"text":"of the Triassic","words":[{"boundingBox":[498,87,505,86,505,96,498,96],"text":"of","confidence":0.983},{"boundingBox":[507,86,522,86,522,97,507,96],"text":"the","confidence":0.987},{"boundingBox":[524,86,559,86,559,97,524,97],"text":"Triassic","confidence":0.981}]},{"boundingBox":[495,97,545,98,545,109,495,108],"text":"land reptile","words":[{"boundingBox":[496,98,515,99,514,109,496,109],"text":"land","confidence":0.985},{"boundingBox":[517,99,546,99,546,109,517,109],"text":"reptile","confidence":0.971}]},{"boundingBox":[373,108,410,107,410,119,374,120],"text":"INDIA","words":[{"boundingBox":[373,108,409,107,410,119,373,120],"text":"INDIA","confidence":0.982}]},{"boundingBox":[498,111,555,111,555,121,498,121],"text":"Lystrosaurus.","words":[{"boundingBox":[498,111,555,112,555,122,498,122],"text":"Lystrosaurus.","confidence":0.896}]},{"boundingBox":[57,213,163,213,163,226,57,226],"text":"SOUTH AMERICA","words":[{"boundingBox":[58,214,102,214,102,227,58,227],"text":"SOUTH","confidence":0.983},{"boundingBox":[104,214,164,213,163,227,104,227],"text":"AMERICA","confidence":0.983}]},{"boundingBox":[472,224,547,224,547,236,472,237],"text":"AUSTRALIA","words":[{"boundingBox":[473,224,547,224,547,237,473,237],"text":"AUSTRALIA","confidence":0.980}]},{"boundingBox":[331,239,412,239,412,251,331,251],"text":"ANTARCTICA","words":[{"boundingBox":[332,239,412,239,413,251,332,252],"text":"ANTARCTICA","confidence":0.963}]},{"boundingBox":[83,323,157,322,157,333,83,334],"text":"Fossil remains of","words":[{"boundingBox":[85,323,108,323,108,334,84,334],"text":"Fossil","confidence":0.984},{"boundingBox":[110,323,145,323,144,334,110,334],"text":"remains","confidence":0.982},{"boundingBox":[147,323,157,323,156,334,146,334],"text":"of","confidence":0.983}]},{"boundingBox":[87,335,151,335,151,347,87,347],"text":"Cynognathus, a","words":[{"boundingBox":[88,335,142,336,142,347,87,347],"text":"Cynognathus,","confidence":0.786},{"boundingBox":[145,336,151,336,151,347,145,347],"text":"a","confidence":0.985}]},{"boundingBox":[464,337,539,336,539,347,464,347],"text":"Fossils of the fern","words":[{"boundingBox":[465,337,492,337,492,348,465,348],"text":"Fossils","confidence":0.983},{"boundingBox":[494,337,502,337,502,348,494,348],"text":"of","confidence":0.988},{"boundingBox":[504,337,517,337,517,348,504,348],"text":"the","confidence":0.987},{"boundingBox":[520,337,540,337,540,348,519,348],"text":"fern","confidence":0.986}]},{"boundingBox":[86,348,169,348,169,359,86,359],"text":"Triassic land reptile","words":[{"boundingBox":[87,348,118,348,117,359,87,359],"text":"Triassic","confidence":0.981},{"boundingBox":[120,348,138,348,138,360,119,359],"text":"land","confidence":0.985},{"boundingBox":[140,348,169,348,169,360,140,360],"text":"reptile","confidence":0.983}]},{"boundingBox":[465,349,544,348,544,360,465,360],"text":"Glossopteris found","words":[{"boundingBox":[466,349,516,349,516,361,465,361],"text":"Glossopteris","confidence":0.849},{"boundingBox":[518,349,544,349,544,360,518,361],"text":"found","confidence":0.985}]},{"boundingBox":[86,361,146,361,146,372,86,372],"text":"approximately","words":[{"boundingBox":[87,362,147,361,147,372,86,372],"text":"approximately","confidence":0.966}]},{"boundingBox":[231,360,318,360,318,371,231,371],"text":"Fossil remains of the","words":[{"boundingBox":[231,360,254,361,254,371,231,371],"text":"Fossil","confidence":0.982},{"boundingBox":[256,361,291,361,290,372,256,371],"text":"remains","confidence":0.980},{"boundingBox":[293,361,301,361,301,372,292,372],"text":"of","confidence":0.987},{"boundingBox":[303,361,319,361,318,371,303,372],"text":"the","confidence":0.987}]},{"boundingBox":[464,361,551,361,551,372,464,372],"text":"in all of the southem","words":[{"boundingBox":[465,362,471,362,471,373,465,373],"text":"in","confidence":0.988},{"boundingBox":[473,362,483,362,483,373,473,373],"text":"all","confidence":0.987},{"boundingBox":[485,362,492,362,492,373,485,373],"text":"of","confidence":0.987},{"boundingBox":[495,362,509,362,509,373,495,373],"text":"the","confidence":0.987},{"boundingBox":[511,362,550,362,550,373,511,373],"text":"southem","confidence":0.951}]},{"boundingBox":[86,372,125,374,124,384,86,383],"text":"3 m long.","words":[{"boundingBox":[86,373,89,373,89,384,86,384],"text":"3","confidence":0.987},{"boundingBox":[91,373,99,373,99,384,91,384],"text":"m","confidence":0.987},{"boundingBox":[101,373,125,374,124,385,101,384],"text":"long.","confidence":0.981}]},{"boundingBox":[231,372,308,373,308,384,231,383],"text":"freshwater reptile","words":[{"boundingBox":[231,373,276,373,276,384,231,383],"text":"freshwater","confidence":0.976},{"boundingBox":[278,373,309,374,308,384,278,384],"text":"reptile","confidence":0.976}]},{"boundingBox":[465,374,555,374,555,385,465,385],"text":"continents, show that","words":[{"boundingBox":[465,375,510,374,510,385,466,385],"text":"continents,","confidence":0.958},{"boundingBox":[512,374,534,374,534,385,512,385],"text":"show","confidence":0.987},{"boundingBox":[536,374,555,375,555,385,536,385],"text":"that","confidence":0.987}]},{"boundingBox":[233,385,286,385,286,396,233,395],"text":"Mesosaurus","words":[{"boundingBox":[233,385,286,386,286,396,233,396],"text":"Mesosaurus","confidence":0.898}]},{"boundingBox":[464,387,560,386,560,398,464,398],"text":"they were once joined.","words":[{"boundingBox":[465,388,481,388,481,398,465,398],"text":"they","confidence":0.987},{"boundingBox":[483,388,505,387,505,398,483,398],"text":"were","confidence":0.987},{"boundingBox":[507,387,528,387,528,398,507,398],"text":"once","confidence":0.980},{"boundingBox":[530,387,560,387,560,398,530,398],"text":"joined.","confidence":0.981}]}]}]}}
```

You should get a response:

```json
{
    "status": "succeeded",
    "original_text": null,
    "text": "SOUTH AMERICA\nFossil remains of Cynognathus, a Triassic land reptile approximately 3 m long.\nAFRICA\nFossil remains of the freshwater reptile Mesosaurus\nINDIA\nANTARCTICA\nFossil evidence of the Triassic land reptile Lystrosaurus.\nAUSTRALIA\nFossils of the fern Glossopteris found in all of the southem continents, show that they were once joined.\n",
    "pages": [
        {
            "id": 1,
            "clockwiseorientation": 0,
            "width": 577,
            "height": 443,
            "unit": "pixel",
            "language": "en",
            "text": "SOUTH AMERICA\nFossil remains of Cynognathus, a Triassic land reptile approximately 3 m long.\nAFRICA\nFossil remains of the freshwater reptile Mesosaurus\nINDIA\nANTARCTICA\nFossil evidence of the Triassic land reptile Lystrosaurus.\nAUSTRALIA\nFossils of the fern Glossopteris found in all of the southem continents, show that they were once joined.",
            "lines": [
                {
                    "start_idx": 7,
                    "end_idx": 7,
                    "boundingbox": [
                        {
                            "X": 58,
                            "Y": 213
                        },
                        {
                            "X": 163,
                            "Y": 213
                        },
                        {
                            "X": 163,
                            "Y": 226
                        },
                        {
                            "X": 58,
                            "Y": 226
                        }
                    ],
                    "text": "SOUTH AMERICA",
                    "words_count": 2,
                    "merged": false,
                    "xmedian": 110.5,
                    "ymedian": 219.5,
                    "end_sentence": false,
                    "avg_height": 13.0,
                    "std_height": 0.0,
                    "rank": 0.0,
                    "cluster": 0,
                    "subcluster": 0,
                    "sorting": [
                        0,
                        0,
                        110.5
                    ]
                },
                {
                    "start_idx": 10,
                    "end_idx": 18,
                    "boundingbox": [
                        {
                            "X": 84,
                            "Y": 322
                        },
                        {
                            "X": 169,
                            "Y": 322
                        },
                        {
                            "X": 169,
                            "Y": 384
                        },
                        {
                            "X": 84,
                            "Y": 384
                        }
                    ],
                    "text": "Fossil remains of Cynognathus, a Triassic land reptile approximately 3 m long.",
                    "words_count": 12,
                    "merged": false,
                    "xmedian": 126.5,
                    "ymedian": 353.5,
                    "end_sentence": true,
                    "avg_height": 11.0,
                    "std_height": 0.0,
                    "rank": 0.0,
                    "cluster": 0,
                    "subcluster": 1,
                    "sorting": [
                        0,
                        1,
                        126.5
                    ]
                },
                {
                    "start_idx": 2,
                    "end_idx": 2,
                    "boundingbox": [
                        {
                            "X": 191,
                            "Y": 84
                        },
                        {
                            "X": 236,
                            "Y": 84
                        },
                        {
                            "X": 236,
                            "Y": 97
                        },
                        {
                            "X": 191,
                            "Y": 97
                        }
                    ],
                    "text": "AFRICA",
                    "words_count": 1,
                    "merged": false,
                    "xmedian": 213.5,
                    "ymedian": 90.5,
                    "end_sentence": false,
                    "avg_height": 12.0,
                    "std_height": 0.0,
                    "rank": 0.0,
                    "cluster": 1,
                    "subcluster": 0,
                    "sorting": [
                        1,
                        0,
                        213.5
                    ]
                },
                {
                    "start_idx": 16,
                    "end_idx": 21,
                    "boundingbox": [
                        {
                            "X": 231,
                            "Y": 360
                        },
                        {
                            "X": 318,
                            "Y": 360
                        },
                        {
                            "X": 318,
                            "Y": 396
                        },
                        {
                            "X": 231,
                            "Y": 396
                        }
                    ],
                    "text": "Fossil remains of the freshwater reptile Mesosaurus",
                    "words_count": 7,
                    "merged": false,
                    "xmedian": 274.5,
                    "ymedian": 378.0,
                    "end_sentence": false,
                    "avg_height": 10.75,
                    "std_height": 0.4330127018922193,
                    "rank": 0.0,
                    "cluster": 1,
                    "subcluster": 1,
                    "sorting": [
                        1,
                        1,
                        274.5
                    ]
                },
                {
                    "start_idx": 5,
                    "end_idx": 5,
                    "boundingbox": [
                        {
                            "X": 373,
                            "Y": 107
                        },
                        {
                            "X": 410,
                            "Y": 107
                        },
                        {
                            "X": 410,
                            "Y": 120
                        },
                        {
                            "X": 373,
                            "Y": 120
                        }
                    ],
                    "text": "INDIA",
                    "words_count": 1,
                    "merged": false,
                    "xmedian": 391.5,
                    "ymedian": 113.5,
                    "end_sentence": false,
                    "avg_height": 12.0,
                    "std_height": 0.0,
                    "rank": 0.0,
                    "cluster": 2,
                    "subcluster": 0,
                    "sorting": [
                        2,
                        0,
                        391.5
                    ]
                },
                {
                    "start_idx": 9,
                    "end_idx": 9,
                    "boundingbox": [
                        {
                            "X": 332,
                            "Y": 239
                        },
                        {
                            "X": 412,
                            "Y": 239
                        },
                        {
                            "X": 412,
                            "Y": 251
                        },
                        {
                            "X": 332,
                            "Y": 251
                        }
                    ],
                    "text": "ANTARCTICA",
                    "words_count": 1,
                    "merged": false,
                    "xmedian": 372.0,
                    "ymedian": 245.0,
                    "end_sentence": false,
                    "avg_height": 13.0,
                    "std_height": 0.0,
                    "rank": 0.0,
                    "cluster": 2,
                    "subcluster": 1,
                    "sorting": [
                        2,
                        1,
                        372.0
                    ]
                },
                {
                    "start_idx": 1,
                    "end_idx": 6,
                    "boundingbox": [
                        {
                            "X": 496,
                            "Y": 73
                        },
                        {
                            "X": 563,
                            "Y": 73
                        },
                        {
                            "X": 563,
                            "Y": 121
                        },
                        {
                            "X": 496,
                            "Y": 121
                        }
                    ],
                    "text": "Fossil evidence of the Triassic land reptile Lystrosaurus.",
                    "words_count": 8,
                    "merged": false,
                    "xmedian": 529.5,
                    "ymedian": 97.0,
                    "end_sentence": true,
                    "avg_height": 10.0,
                    "std_height": 0.0,
                    "rank": 0.0,
                    "cluster": 3,
                    "subcluster": 0,
                    "sorting": [
                        3,
                        0,
                        529.5
                    ]
                },
                {
                    "start_idx": 8,
                    "end_idx": 8,
                    "boundingbox": [
                        {
                            "X": 473,
                            "Y": 224
                        },
                        {
                            "X": 547,
                            "Y": 224
                        },
                        {
                            "X": 547,
                            "Y": 237
                        },
                        {
                            "X": 473,
                            "Y": 237
                        }
                    ],
                    "text": "AUSTRALIA",
                    "words_count": 1,
                    "merged": false,
                    "xmedian": 510.0,
                    "ymedian": 230.0,
                    "end_sentence": false,
                    "avg_height": 13.0,
                    "std_height": 0.0,
                    "rank": 0.0,
                    "cluster": 3,
                    "subcluster": 1,
                    "sorting": [
                        3,
                        1,
                        510.0
                    ]
                },
                {
                    "start_idx": 12,
                    "end_idx": 22,
                    "boundingbox": [
                        {
                            "X": 465,
                            "Y": 336
                        },
                        {
                            "X": 560,
                            "Y": 336
                        },
                        {
                            "X": 560,
                            "Y": 398
                        },
                        {
                            "X": 465,
                            "Y": 398
                        }
                    ],
                    "text": "Fossils of the fern Glossopteris found in all of the southem continents, show that they were once joined.",
                    "words_count": 18,
                    "merged": false,
                    "xmedian": 512.5,
                    "ymedian": 367.5,
                    "end_sentence": true,
                    "avg_height": 11.0,
                    "std_height": 0.0,
                    "rank": 0.0,
                    "cluster": 3,
                    "subcluster": 2,
                    "sorting": [
                        3,
                        2,
                        512.5
                    ]
                }
            ],
            "ppi": 1
        }
    ]
}
```

## Upload Docker Image to Azure 

We will be uploading the docker image to the Azure Container Registry.  In a subsequent step we will be deploying the docker container to an Azure Web App, however this registry has the nice aspect that it allows us to do contiunous deployment so whenever we add an updated container to the registry it will automatically update the running container.

* [Create an Azure Container registry](https://docs.microsoft.com/en-us/azure/container-registry/container-registry-get-started-portal)
* Once the registry is created, open it "Access Keys" in the Settings and make note of the Login Server, Username and one of the passwords
* From your desktop in the Azure Command Prompt login to your Azure Subscription by typing: <code>az login</code>
* Log in to your Azure container registry by typing: <code>docker login [Login Server]</code> where [Login Server] is the value taken from the above step.  If this is the first time logging in to your container registry, you will need to enter the above username and password.
* Tag the local container: <code>docker tag ocrlayout [Login Server]/puthurr/ocrlayout</code>
* Upload the tagged container: <code>docker push [Login Server]/puthurr/ocrlayout</code>

## Deploy the Docker Image to an Azure Web App

There are numerous ways to run a docker container in Azure, we will use Azure Web Apps because it allowed me to add an HTTPS endpoint. To do this: 

* From Azure Portal, create a "Web App", which is located under the "Web" section of the Azure Marketplace.  Make sure it is in the sam subscription as that of your Azure Container Registry.
* In the Basics configuration tab, enter the details, ensuring:
    * Publish: Docker Image
    * Operating System: Linux
    * App service plan need to be one that allows for HTTPS
* In the Basics configuration tab, enter the details, ensuring:
    * Image Source: Azure Container Registry
    * Publish: Docker Image
    * Registry ==> Choose your Azure Container Registry
    * Image ==> Choose your Azure Container Image
    * Tag: Latest

## Wait for Image to come Online
Just because the Web App is created, does not mean the container is ready.  To monitor the progress:
* In the portal for the Web App you just created, choose "Container Settings" and in the Logs, scroll down to the bottom. You will see a lot of lines indicating it is downloading the image.  Keep choosing "Refresh" until you see something like:
<code>
2019-06-12 23:32:14.243 INFO  - Initiating warmup request to container XXX-container-kp_0 for site liamca-container-kp
2019-06-12 23:32:30.573 INFO  - Container XXX-container-kp_0 for site liamca-container-kp initialized successfully and is ready to serve requests.
</code>

* Optional: I like to set "Continuous Deployment" to On so than any container uploaded replaces the running one.

## Test the Azure Docker Image
After the docker image is created, go to the resource and make note of the URL which will be something like: https:[foo].azurewebsites.net
    
POST: [URL from last Section]/azureocr
Header: 
<code>Content-Type: application/json</code>
Body (raw): 
```json
{"status":"succeeded","createdDateTime":"2020-06-07T19:01:37Z","lastUpdatedDateTime":"2020-06-07T19:01:38Z","analyzeResult":{"version":"3.0.0","readResults":[{"page":1,"language":"en","angle":0,"width":577,"height":443,"unit":"pixel","lines":[{"boundingBox":[498,73,563,73,563,84,498,83],"text":"Fossil evidence","words":[{"boundingBox":[498,74,521,74,521,84,498,84],"text":"Fossil","confidence":0.976},{"boundingBox":[523,74,564,74,563,84,523,84],"text":"evidence","confidence":0.981}]},{"boundingBox":[190,84,236,84,236,97,190,97],"text":"AFRICA","words":[{"boundingBox":[191,85,236,85,236,97,191,97],"text":"AFRICA","confidence":0.983}]},{"boundingBox":[498,86,558,85,559,96,498,96],"text":"of the Triassic","words":[{"boundingBox":[498,87,505,86,505,96,498,96],"text":"of","confidence":0.983},{"boundingBox":[507,86,522,86,522,97,507,96],"text":"the","confidence":0.987},{"boundingBox":[524,86,559,86,559,97,524,97],"text":"Triassic","confidence":0.981}]},{"boundingBox":[495,97,545,98,545,109,495,108],"text":"land reptile","words":[{"boundingBox":[496,98,515,99,514,109,496,109],"text":"land","confidence":0.985},{"boundingBox":[517,99,546,99,546,109,517,109],"text":"reptile","confidence":0.971}]},{"boundingBox":[373,108,410,107,410,119,374,120],"text":"INDIA","words":[{"boundingBox":[373,108,409,107,410,119,373,120],"text":"INDIA","confidence":0.982}]},{"boundingBox":[498,111,555,111,555,121,498,121],"text":"Lystrosaurus.","words":[{"boundingBox":[498,111,555,112,555,122,498,122],"text":"Lystrosaurus.","confidence":0.896}]},{"boundingBox":[57,213,163,213,163,226,57,226],"text":"SOUTH AMERICA","words":[{"boundingBox":[58,214,102,214,102,227,58,227],"text":"SOUTH","confidence":0.983},{"boundingBox":[104,214,164,213,163,227,104,227],"text":"AMERICA","confidence":0.983}]},{"boundingBox":[472,224,547,224,547,236,472,237],"text":"AUSTRALIA","words":[{"boundingBox":[473,224,547,224,547,237,473,237],"text":"AUSTRALIA","confidence":0.980}]},{"boundingBox":[331,239,412,239,412,251,331,251],"text":"ANTARCTICA","words":[{"boundingBox":[332,239,412,239,413,251,332,252],"text":"ANTARCTICA","confidence":0.963}]},{"boundingBox":[83,323,157,322,157,333,83,334],"text":"Fossil remains of","words":[{"boundingBox":[85,323,108,323,108,334,84,334],"text":"Fossil","confidence":0.984},{"boundingBox":[110,323,145,323,144,334,110,334],"text":"remains","confidence":0.982},{"boundingBox":[147,323,157,323,156,334,146,334],"text":"of","confidence":0.983}]},{"boundingBox":[87,335,151,335,151,347,87,347],"text":"Cynognathus, a","words":[{"boundingBox":[88,335,142,336,142,347,87,347],"text":"Cynognathus,","confidence":0.786},{"boundingBox":[145,336,151,336,151,347,145,347],"text":"a","confidence":0.985}]},{"boundingBox":[464,337,539,336,539,347,464,347],"text":"Fossils of the fern","words":[{"boundingBox":[465,337,492,337,492,348,465,348],"text":"Fossils","confidence":0.983},{"boundingBox":[494,337,502,337,502,348,494,348],"text":"of","confidence":0.988},{"boundingBox":[504,337,517,337,517,348,504,348],"text":"the","confidence":0.987},{"boundingBox":[520,337,540,337,540,348,519,348],"text":"fern","confidence":0.986}]},{"boundingBox":[86,348,169,348,169,359,86,359],"text":"Triassic land reptile","words":[{"boundingBox":[87,348,118,348,117,359,87,359],"text":"Triassic","confidence":0.981},{"boundingBox":[120,348,138,348,138,360,119,359],"text":"land","confidence":0.985},{"boundingBox":[140,348,169,348,169,360,140,360],"text":"reptile","confidence":0.983}]},{"boundingBox":[465,349,544,348,544,360,465,360],"text":"Glossopteris found","words":[{"boundingBox":[466,349,516,349,516,361,465,361],"text":"Glossopteris","confidence":0.849},{"boundingBox":[518,349,544,349,544,360,518,361],"text":"found","confidence":0.985}]},{"boundingBox":[86,361,146,361,146,372,86,372],"text":"approximately","words":[{"boundingBox":[87,362,147,361,147,372,86,372],"text":"approximately","confidence":0.966}]},{"boundingBox":[231,360,318,360,318,371,231,371],"text":"Fossil remains of the","words":[{"boundingBox":[231,360,254,361,254,371,231,371],"text":"Fossil","confidence":0.982},{"boundingBox":[256,361,291,361,290,372,256,371],"text":"remains","confidence":0.980},{"boundingBox":[293,361,301,361,301,372,292,372],"text":"of","confidence":0.987},{"boundingBox":[303,361,319,361,318,371,303,372],"text":"the","confidence":0.987}]},{"boundingBox":[464,361,551,361,551,372,464,372],"text":"in all of the southem","words":[{"boundingBox":[465,362,471,362,471,373,465,373],"text":"in","confidence":0.988},{"boundingBox":[473,362,483,362,483,373,473,373],"text":"all","confidence":0.987},{"boundingBox":[485,362,492,362,492,373,485,373],"text":"of","confidence":0.987},{"boundingBox":[495,362,509,362,509,373,495,373],"text":"the","confidence":0.987},{"boundingBox":[511,362,550,362,550,373,511,373],"text":"southem","confidence":0.951}]},{"boundingBox":[86,372,125,374,124,384,86,383],"text":"3 m long.","words":[{"boundingBox":[86,373,89,373,89,384,86,384],"text":"3","confidence":0.987},{"boundingBox":[91,373,99,373,99,384,91,384],"text":"m","confidence":0.987},{"boundingBox":[101,373,125,374,124,385,101,384],"text":"long.","confidence":0.981}]},{"boundingBox":[231,372,308,373,308,384,231,383],"text":"freshwater reptile","words":[{"boundingBox":[231,373,276,373,276,384,231,383],"text":"freshwater","confidence":0.976},{"boundingBox":[278,373,309,374,308,384,278,384],"text":"reptile","confidence":0.976}]},{"boundingBox":[465,374,555,374,555,385,465,385],"text":"continents, show that","words":[{"boundingBox":[465,375,510,374,510,385,466,385],"text":"continents,","confidence":0.958},{"boundingBox":[512,374,534,374,534,385,512,385],"text":"show","confidence":0.987},{"boundingBox":[536,374,555,375,555,385,536,385],"text":"that","confidence":0.987}]},{"boundingBox":[233,385,286,385,286,396,233,395],"text":"Mesosaurus","words":[{"boundingBox":[233,385,286,386,286,396,233,396],"text":"Mesosaurus","confidence":0.898}]},{"boundingBox":[464,387,560,386,560,398,464,398],"text":"they were once joined.","words":[{"boundingBox":[465,388,481,388,481,398,465,398],"text":"they","confidence":0.987},{"boundingBox":[483,388,505,387,505,398,483,398],"text":"were","confidence":0.987},{"boundingBox":[507,387,528,387,528,398,507,398],"text":"once","confidence":0.980},{"boundingBox":[530,387,560,387,560,398,530,398],"text":"joined.","confidence":0.981}]}]}]}}
```

You should get the same response you did when running it locally (beautified for reading convenience):
```json
{
    "status": "succeeded",
    "original_text": null,
    "text": "SOUTH AMERICA\nFossil remains of Cynognathus, a Triassic land reptile approximately 3 m long.\nAFRICA\nFossil remains of the freshwater reptile Mesosaurus\nINDIA\nANTARCTICA\nFossil evidence of the Triassic land reptile Lystrosaurus.\nAUSTRALIA\nFossils of the fern Glossopteris found in all of the southem continents, show that they were once joined.\n",
    "pages": [
        {
            "id": 1,
            "clockwiseorientation": 0,
            "width": 577,
            "height": 443,
            "unit": "pixel",
            "language": "en",
            "text": "SOUTH AMERICA\nFossil remains of Cynognathus, a Triassic land reptile approximately 3 m long.\nAFRICA\nFossil remains of the freshwater reptile Mesosaurus\nINDIA\nANTARCTICA\nFossil evidence of the Triassic land reptile Lystrosaurus.\nAUSTRALIA\nFossils of the fern Glossopteris found in all of the southem continents, show that they were once joined.",
            "lines": [
                {
                    "start_idx": 7,
                    "end_idx": 7,
                    "boundingbox": [
                        {
                            "X": 58,
                            "Y": 213
                        },
                        {
                            "X": 163,
                            "Y": 213
                        },
                        {
                            "X": 163,
                            "Y": 226
                        },
                        {
                            "X": 58,
                            "Y": 226
                        }
                    ],
                    "text": "SOUTH AMERICA",
                    "words_count": 2,
                    "merged": false,
                    "xmedian": 110.5,
                    "ymedian": 219.5,
                    "end_sentence": false,
                    "avg_height": 13.0,
                    "std_height": 0.0,
                    "rank": 0.0,
                    "cluster": 0,
                    "subcluster": 0,
                    "sorting": [
                        0,
                        0,
                        110.5
                    ]
                },
                {
                    "start_idx": 10,
                    "end_idx": 18,
                    "boundingbox": [
                        {
                            "X": 84,
                            "Y": 322
                        },
                        {
                            "X": 169,
                            "Y": 322
                        },
                        {
                            "X": 169,
                            "Y": 384
                        },
                        {
                            "X": 84,
                            "Y": 384
                        }
                    ],
                    "text": "Fossil remains of Cynognathus, a Triassic land reptile approximately 3 m long.",
                    "words_count": 12,
                    "merged": false,
                    "xmedian": 126.5,
                    "ymedian": 353.5,
                    "end_sentence": true,
                    "avg_height": 11.0,
                    "std_height": 0.0,
                    "rank": 0.0,
                    "cluster": 0,
                    "subcluster": 1,
                    "sorting": [
                        0,
                        1,
                        126.5
                    ]
                },
                {
                    "start_idx": 2,
                    "end_idx": 2,
                    "boundingbox": [
                        {
                            "X": 191,
                            "Y": 84
                        },
                        {
                            "X": 236,
                            "Y": 84
                        },
                        {
                            "X": 236,
                            "Y": 97
                        },
                        {
                            "X": 191,
                            "Y": 97
                        }
                    ],
                    "text": "AFRICA",
                    "words_count": 1,
                    "merged": false,
                    "xmedian": 213.5,
                    "ymedian": 90.5,
                    "end_sentence": false,
                    "avg_height": 12.0,
                    "std_height": 0.0,
                    "rank": 0.0,
                    "cluster": 1,
                    "subcluster": 0,
                    "sorting": [
                        1,
                        0,
                        213.5
                    ]
                },
                {
                    "start_idx": 16,
                    "end_idx": 21,
                    "boundingbox": [
                        {
                            "X": 231,
                            "Y": 360
                        },
                        {
                            "X": 318,
                            "Y": 360
                        },
                        {
                            "X": 318,
                            "Y": 396
                        },
                        {
                            "X": 231,
                            "Y": 396
                        }
                    ],
                    "text": "Fossil remains of the freshwater reptile Mesosaurus",
                    "words_count": 7,
                    "merged": false,
                    "xmedian": 274.5,
                    "ymedian": 378.0,
                    "end_sentence": false,
                    "avg_height": 10.75,
                    "std_height": 0.4330127018922193,
                    "rank": 0.0,
                    "cluster": 1,
                    "subcluster": 1,
                    "sorting": [
                        1,
                        1,
                        274.5
                    ]
                },
                {
                    "start_idx": 5,
                    "end_idx": 5,
                    "boundingbox": [
                        {
                            "X": 373,
                            "Y": 107
                        },
                        {
                            "X": 410,
                            "Y": 107
                        },
                        {
                            "X": 410,
                            "Y": 120
                        },
                        {
                            "X": 373,
                            "Y": 120
                        }
                    ],
                    "text": "INDIA",
                    "words_count": 1,
                    "merged": false,
                    "xmedian": 391.5,
                    "ymedian": 113.5,
                    "end_sentence": false,
                    "avg_height": 11.0,
                    "std_height": 0.0,
                    "rank": 0.0,
                    "cluster": 2,
                    "subcluster": 0,
                    "sorting": [
                        2,
                        0,
                        391.5
                    ]
                },
                {
                    "start_idx": 9,
                    "end_idx": 9,
                    "boundingbox": [
                        {
                            "X": 332,
                            "Y": 239
                        },
                        {
                            "X": 412,
                            "Y": 239
                        },
                        {
                            "X": 412,
                            "Y": 251
                        },
                        {
                            "X": 332,
                            "Y": 251
                        }
                    ],
                    "text": "ANTARCTICA",
                    "words_count": 1,
                    "merged": false,
                    "xmedian": 372.0,
                    "ymedian": 245.0,
                    "end_sentence": false,
                    "avg_height": 12.0,
                    "std_height": 0.0,
                    "rank": 0.0,
                    "cluster": 2,
                    "subcluster": 1,
                    "sorting": [
                        2,
                        1,
                        372.0
                    ]
                },
                {
                    "start_idx": 1,
                    "end_idx": 6,
                    "boundingbox": [
                        {
                            "X": 496,
                            "Y": 73
                        },
                        {
                            "X": 563,
                            "Y": 73
                        },
                        {
                            "X": 563,
                            "Y": 121
                        },
                        {
                            "X": 496,
                            "Y": 121
                        }
                    ],
                    "text": "Fossil evidence of the Triassic land reptile Lystrosaurus.",
                    "words_count": 8,
                    "merged": false,
                    "xmedian": 529.5,
                    "ymedian": 97.0,
                    "end_sentence": true,
                    "avg_height": 10.0,
                    "std_height": 0.0,
                    "rank": 0.0,
                    "cluster": 3,
                    "subcluster": 0,
                    "sorting": [
                        3,
                        0,
                        529.5
                    ]
                },
                {
                    "start_idx": 8,
                    "end_idx": 8,
                    "boundingbox": [
                        {
                            "X": 473,
                            "Y": 224
                        },
                        {
                            "X": 547,
                            "Y": 224
                        },
                        {
                            "X": 547,
                            "Y": 237
                        },
                        {
                            "X": 473,
                            "Y": 237
                        }
                    ],
                    "text": "AUSTRALIA",
                    "words_count": 1,
                    "merged": false,
                    "xmedian": 510.0,
                    "ymedian": 230.0,
                    "end_sentence": false,
                    "avg_height": 13.0,
                    "std_height": 0.0,
                    "rank": 0.0,
                    "cluster": 3,
                    "subcluster": 1,
                    "sorting": [
                        3,
                        1,
                        510.0
                    ]
                },
                {
                    "start_idx": 12,
                    "end_idx": 22,
                    "boundingbox": [
                        {
                            "X": 465,
                            "Y": 336
                        },
                        {
                            "X": 560,
                            "Y": 336
                        },
                        {
                            "X": 560,
                            "Y": 398
                        },
                        {
                            "X": 465,
                            "Y": 398
                        }
                    ],
                    "text": "Fossils of the fern Glossopteris found in all of the southem continents, show that they were once joined.",
                    "words_count": 18,
                    "merged": false,
                    "xmedian": 512.5,
                    "ymedian": 367.5,
                    "end_sentence": true,
                    "avg_height": 11.0,
                    "std_height": 0.0,
                    "rank": 0.0,
                    "cluster": 3,
                    "subcluster": 2,
                    "sorting": [
                        3,
                        2,
                        512.5
                    ]
                }
            ],
            "ppi": 1
        }
    ]
}
```

## Send an ocr response using curl 
Adjust the endpoint port accordingly. 
>Don't forget to send the width and height of the image for AWS OCR processing. 

Image253 is of width 577 and height 443. 
```
curl -i -H "Content-Type: application/json" -X POST -d @ocr_jsons/image253.azure.read.json http://localhost/azureocr
curl -i -H "Content-Type: application/json" -X POST -d @ocr_jsons/image253.google.vision.json http://localhost/googleocr
curl -i -H "Content-Type: application/json" -X POST -d @ocr_jsons/image253.aws.textextract.json "http://localhost/awsocr?width=577&height=443"
```
scan3 is of width 674 and height 1015. 
```
curl -i -H "Content-Type: application/json" -X POST -d @ocr_jsons/scan3.azure.read.json http://localhost/azureocr
curl -i -H "Content-Type: application/json" -X POST -d @ocr_jsons/scan3.google.vision.json http://localhost/googleocr
curl -i -H "Content-Type: application/json" -X POST -d @ocr_jsons/scan3.aws.textextract.json "http://localhost/awsocr?width=674&height=1015"
```
