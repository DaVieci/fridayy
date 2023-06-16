#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 20:30:43 2021

@author: DaVieci
"""

import speech_recognition as sr


r = sr.Recognizer()

with sr.Microphone() as source:
    print("Ja, bitte?")
    audio_text = r.listen(source)
    print("Okay, einen Moment..")
    try:
        rec_text = r.recognize_google(audio_text, language = "de-DE")
        print("- \""+rec_text+"\"")
    except:
         print("Tut mir Leid, ich konnte das nicht verstehen.")