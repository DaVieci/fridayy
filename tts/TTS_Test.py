#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 30 18:00:43 2021

@author: DaVieci
"""

from gtts import gTTS
import os


spoken_text = "Hallo, wie kann ich Ihnen behilflich sein?"
file = "hallo.mp3"
tts = gTTS(text=spoken_text, lang='de')

tts.save(file)
print(spoken_text)
os.system("mpg321 " +file+" &>/dev/null")
os.system("rm "+file)
