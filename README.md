# OCRLAYOUT  Recipes 

>This repository provides clear examples of the value of **ocrlayout** with real-world examples. 

## OCRLAYOUT Problem Statement reminder
Current OCR engines responses are focus on text recall. Ocrlayout tries to go a step further by re-ordering the lines of text so it'd approach a human-reading behavior. 

When images contains a lot of textual information, it becomes relevant to assemble the generated meaninful blocks of text enabling better scenarios. 

Another way to see would be to cluster the lines of text based on their positions/coordinates in the original content. 
## More meaningfull output for what? 
- **Text Analytics** you may leverage any Text Analytics such as Key Phrases, Entities Extraction with more confidence of its outcome
- **Accessibility** : Any infographic becomes alive, overcoming the alt text feature.
- **Read Aloud feature** : it becomes easier to build solutions to read aloud an image, increasing verbal narrative of visual information. 
- **Machine Translation** : get more accurate MT output as you can retain more context. 
- **Sentences/Paragraph Classification**: from scanned-base images i.e. contracts, having a more meaninful textual output allows you to classify it at a granular level in terms of risk, personal clause or conditions. 

## More meaningful for Text Analytics 
Combined with Spacy, you can prove the value of ocrlayout by extracting clear sentences, extract clearer entities, train NL model etc. 

## More meaningful for Accessibility 
Once you have a clearer text output, you might want to create an audio file to read that text

Check out the generated audio in the below examples
[Example1](https://puthurr.github.io/examples/scan1/#accessibility)
[Example2](https://puthurr.github.io/examples/scan6/#accessibility)
[Example3](https://puthurr.github.io/examples/scan2/#accessibility)

Our recipe uses Azure Text to Speech cognitive service. Its current SDK limits the duration of the audio you get to 10min. To create a full audio book a new API is currently in preview: 

>Unlike the text to speech API that's used by the Speech SDK, the Long Audio API can create synthesized audio longer than 10 minutes, making it ideal for publishers and audio content platforms.

https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/long-audio-api

## More meaningful output for Translation
As for the Text to Speech, you may translate your text output with better confidence. 

[Azure Translator Service](https://github.com/MicrosoftTranslator/Text-Translation-API-V3-Python)

## Integration Scenario

# Docker Flask recipe
Check how easy it is to create a service out of ocrlayout, serve through Flask and deployed as a Docker container. 

# Azure Cognitive Search Custom Skill
One of the application of ocrlayout is Azure Cognitive Search. While processing embedded images, you can leverage ocrlayout to creaet better textual recognition metadata, translate them into another language or configure Text Analytics on top of it. 
