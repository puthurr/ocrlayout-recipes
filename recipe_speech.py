import sys
import os
import azure.cognitiveservices.speech as speechsdk
from pathlib import Path
# Copied from 
# https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/f356a22eda60717aec95f1a9becf6f5bbfbf8aca/samples/python/console/speech_synthesis_sample.py
#
speech_key = os.environ.get("COMPUTERVISION_SUBSCRIPTION_KEY", None)
service_region = os.environ.get("COMPUTERVISION_LOCATION", "westeurope")

IMAGES_FOLDER = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), "./images")

RESULTS_FOLDER = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), "./tests-results")

def iterate_all_images(filter=None):
    """
    Iterate through all images located in the IMAGES_FOLDER
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

        with open(os.path.join(RESULTS_FOLDER, imgname+".azure.read.after.txt"), 'r') as cachefile:
            ocrresponse = cachefile.read().replace('\n', '')

        if "de_" in imgname:
            speech_synthesis_with_language(imgname,ocrresponse,language="de-DE",voice="de-DE-KatjaNeural")
        elif "en_" in imgname:
            speech_synthesis_with_language(imgname,ocrresponse,language="en-US",voice="en-AU-NatashaNeural")

def speech_synthesis_with_language(input_doc_name,input_doc,language,voice):
    """performs speech synthesis to the default speaker with specified spoken language"""
    # Creates an instance of a speech config with specified subscription key and service region.
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    # Sets the synthesis language.
    # The full list of supported languages can be found here:
    # https://docs.microsoft.com/azure/cognitive-services/speech-service/language-support#text-to-speech
    speech_config.speech_synthesis_language = language

    if voice:
        speech_config.speech_synthesis_voice_name = voice

    # Sets the synthesis output format.
    # The full list of supported format can be found here:
    # https://docs.microsoft.com/azure/cognitive-services/speech-service/rest-text-to-speech#audio-outputs
    speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3)

    # Creates a speech synthesizer using file as audio output.
    # Replace with your own audio file name.
    file_name = os.path.join(RESULTS_FOLDER,input_doc_name+"."+language+".mp3")
    file_config = speechsdk.audio.AudioOutputConfig(filename=file_name)

    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=file_config)

    # Get the text from ocrlayout output 
    result = speech_synthesizer.speak_text_async(input_doc).get()
    # Check result
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized to speaker for text [{}] with language [{}]".format(input_doc, language))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))

if __name__ == "__main__":
    import sys, os.path
    sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..", "..")))
    import os

    if not os.path.exists(RESULTS_FOLDER):
        os.makedirs(RESULTS_FOLDER)

    # Process all images contained the IMAGES_FOLDER
    iterate_all_images()
