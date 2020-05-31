# pip install spacy
# python -m spacy download en_core_web_sm
import json
import os
import sys
import types
from pathlib import Path

import spacy
from spacy import displacy

IMAGES_FOLDER = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), "./images")

RESULTS_FOLDER = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), "./tests-results")

def iterate_all_images(filter=None):
    """OCR Text detection for all images 
    Iterate through all images located in the IMAGES_FOLDER and call all OCR Engines
    """
    for filename in os.listdir(IMAGES_FOLDER):
        if filter:
            if filter not in filename:
                continue
        if '.DS_Store' in filename:
            continue

        print("AZURE Image Name {}".format(filename))
        p = Path(filename)
        (imgname,imgext) = os.path.splitext(p.name)

        # Get the BEFORE output
        with open(os.path.join(RESULTS_FOLDER, imgname+".azure.read.before.txt"), 'r') as cachefile:
            orig = cachefile.read().replace('\n', '')

        # Get the AFTER output
        with open(os.path.join(RESULTS_FOLDER, imgname+".azure.read.after.txt"), 'r') as cachefile:
            new = cachefile.read().replace('\n', '')

        doc1=spacy_me(imgname,orig,"before")
        html1 = displacy.render(doc1,style="ent",page=True)
        with open(os.path.join(RESULTS_FOLDER, imgname+".before.spacy.entities.html"), 'w') as outfile:
            outfile.write(html1)

        doc2=spacy_me(imgname,new,"after")
        html2 = displacy.render(doc2,style="ent",page=True)
        with open(os.path.join(RESULTS_FOLDER, imgname+".after.spacy.entities.html"), 'w') as outfile:
            outfile.write(html2)

def spacy_me(input_doc_name,input_doc,log_prefix):

    if "en_" in input_doc_name:
        # Load English tokenizer, log_prefixger, parser, NER and word vectors
        nlp = spacy.load("en_core_web_sm")
    elif "de_" in input_doc_name:
        nlp = spacy.load("de_core_news_sm")

    doc = nlp(input_doc)
    # Analyze syntax
    print(log_prefix+"|Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
    print(log_prefix+"|Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])

    # Find named entities, phrases and concepts
    entities=[]
    for entity in doc.ents:
        entities.append(entity.text+" "+entity.label_)
    with open(os.path.join(RESULTS_FOLDER, input_doc_name+"."+log_prefix+".spacy.named_entities.json"), 'w') as outfile:
        outfile.write("\n".join(sorted(entities)))
    # Extract the sentences...
    sentences=[]
    for sent in doc.sents:
        sentences.append(sent.text)
    with open(os.path.join(RESULTS_FOLDER, input_doc_name+"."+log_prefix+".spacy.sentences.json"), 'w') as outfile:
        outfile.write("\n".join(sentences))

    doc.user_data["title"] = (input_doc_name+"."+log_prefix)
    return doc

if __name__ == "__main__":
    import sys, os.path
    sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..", "..")))
    import os

    if not os.path.exists(RESULTS_FOLDER):
        os.makedirs(RESULTS_FOLDER)

    # Process all images contained the IMAGES_FOLDER
    iterate_all_images()
