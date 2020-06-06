# AZURE - OCRLayout standalone container service built using Docker, Python and Flask 

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
```

You should get a response:

```json
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
```
You should get the same response you did when running it locally:
```json
```

## Send an azure ocr response using curl 

Adjust the endpoint port. 

This will upload the JSON created by running the recipe-start.py script. 

<code>curl -i -H "Content-Type: application/json" -X POST -d @en_scan4.azure.read.json http://localhost:5000/azureocr</code>

<code>curl -i -H "Content-Type: application/json" -X POST -d @en_scan4.azure.read.json http://localhost:5005/azureocr</code>
