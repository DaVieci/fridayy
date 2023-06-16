#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 20:11:19 2021

@author: DaVieci
"""

#import library
import speech_recognition as sr


file = 'hallo.wav'
r = sr.Recognizer()

with sr.AudioFile(file) as source:
    audio_text = r.listen(source)
    try:
        print('Starte Spracherkennung für', file)
        text = r.recognize_google(audio_text, language = "de-DE")
        print('Erkannter Text:', text)
    except:
         print('Tut mir Leid, ich konnte das nicht verstehen.')
