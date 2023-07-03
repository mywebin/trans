import os
import azure.cognitiveservices.speech as speechsdk
import streamlit as st


speech_translation_config = speechsdk.translation.SpeechTranslationConfig(subscription='9dda1165566445f18bd86d7d1f589ae2', region='centralindia')
speech_translation_config.speech_recognition_language='en-IN'

test_dict = {"hi-IN": "hi-IN-MadhurNeural", "te-IN": "te-IN-MohanNeural", "en-IN": "en-IN-PrabhatNeural","ar-SA" :"ar-SA-HamedNeural"}



def recognize_from_microphone(from_lang="en-IN", to_lang="hi-IN"):
    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    

    target_language=to_lang
    speech_translation_config.add_target_language(target_language)

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    translation_recognizer = speechsdk.translation.TranslationRecognizer(translation_config=speech_translation_config, audio_config=audio_config)

    print("Speak into your microphone.")
    translation_recognition_result = translation_recognizer.recognize_once_async().get()

    if translation_recognition_result.reason == speechsdk.ResultReason.TranslatedSpeech:
        st.write("Recognized: {}".format(translation_recognition_result.text))
        
        text = translation_recognition_result.translations[target_language]
        st.write("""Translated into '{}': {}""".format(
            target_language, text))
        speak_out(text, 'hi-IN-MadhurNeural')
    elif translation_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(translation_recognition_result.no_match_details))
    elif translation_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = translation_recognition_result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")
    



# recognize_from_microphone()




# This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
speech_config = speechsdk.SpeechConfig(subscription='9dda1165566445f18bd86d7d1f589ae2', region='centralindia')
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

def speak_out(text, to_lang="en-US-JennyNeural"):
    # The language of the voice that speaks.
    speech_config.speech_synthesis_voice_name=to_lang
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    # Get text from the console and synthesize to the default speaker.
#print("Enter some text that you want to speak >")
#text = input()

    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized for text [{}]".format(text))
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")



st.title('Voice Translate App')
st.write("Speak into your microphone.")

from_option = st.selectbox(
     'What is your language input',
    ('en-IN', 'te-IN', 'hi'))

st.write('You selected:', from_option)


to_option = st.selectbox(
     'Whai do you want to translate to?',
    ('en', 'te', 'hi'))

st.write('You selected:', to_option)

#st.write("Select Input Language")

#st.selectbox(label, options, index=0, format_func=special_internal_function, key=None, help=None, on_change=None, args=None, kwargs=None, *, disabled=False, label_visibility="visible")

#st.write("Select Output Language")
#st.selectbox(label, options, index=0, format_func=special_internal_function, key=None, help=None, on_change=None, args=None, kwargs=None, *, disabled=False, label_visibility="visible")



recognize_from_microphone(from_option, to_option)


