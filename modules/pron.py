import os
import azure.cognitiveservices.speech as speechsdk

def get_pronunciation(path, word):
    speech_config = speechsdk.SpeechConfig(subscription=os.environ['AZURE_SPEECH_APIKEY'], region=os.environ['AZURE_SPEECH_APIREGION'])
    speech_config.speech_recognition_language="zh-TW"
    audio_config = speechsdk.audio.AudioConfig(filename=path)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, language="zh-TW", audio_config=audio_config)
    pronunciation_config = speechsdk.PronunciationAssessmentConfig(reference_text=word, grading_system=speechsdk.PronunciationAssessmentGradingSystem.HundredMark, granularity=speechsdk.PronunciationAssessmentGranularity.Phoneme, enable_miscue=True)

    pronunciation_config.apply_to(speech_recognizer)
    speech_recognition_result = speech_recognizer.recognize_once()

    pronunciation_assessment_result_json = speech_recognition_result.properties.get(speechsdk.PropertyId.SpeechServiceResponse_JsonResult)
    return pronunciation_assessment_result_json