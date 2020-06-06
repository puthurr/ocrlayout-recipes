FROM python:3.7-slim
RUN apt-get update && apt-get install -y python3-pip
RUN apt-get update && apt-get install -y libsm6 libxext6 libxrender-dev
COPY . /storage-emulator
WORKDIR /storage-emulator

# RUN pip3 install pyopenssl
RUN pip3 install -r requirements.txt

EXPOSE 80
ENTRYPOINT ["python"]
CMD ["ocrlayout-ws.py"]