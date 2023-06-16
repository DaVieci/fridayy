#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import speech_recognition as sr


class STT:
    
    def __init__(self):
        self.__recognizer = sr.Recognizer()
        self.__audio_text = None
    
    def start_mic_listening(self):
        with sr.Microphone() as source:
            self.__audio_text = self.__recognizer.listen(source)
    
    def get_text_from_recognized_speech(self):
        try:
            text = self.__recognizer.recognize_google(self.__audio_text, language="de-DE")
        except:
            text = -1
        return text
