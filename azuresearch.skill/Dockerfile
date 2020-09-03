FROM python:3.7-slim
RUN apt-get update && apt-get install -y python3-pip
RUN apt-get update && apt-get install -y libsm6 libxext6 libxrender-dev
COPY . /storage-emulator
WORKDIR /storage-emulator

# RUN pip3 install pyopenssl
RUN pip3 install -r requirements.txt

# RUN python -m nltk.downloader stopwords
# RUN python -m nltk.downloader universal_tagset
# RUN python -m spacy download en 

EXPOSE 5005
ENTRYPOINT ["python"]
CMD ["ocrlayout-skill.py"]