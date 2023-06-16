#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import time
from pathlib import Path
from pygame import mixer

from gtts import gTTS


class TTS:
    
    def __init__(self):
        self.__audio_dir = "tts/audio-logs/"
    
    def get_speech_file_from_text(self, text):
        audio_file = self.__create_audio_file()
        tts = gTTS(text=text, lang='de')
        tts.save(audio_file)
        return audio_file
    
    def play_speech_file(self, file):
        mixer.init()
        mixer.music.load(file)
        mixer.music.play()
        self.__wait_until_track_has_finished()
    
    def __create_audio_file(self):
        timestamp = datetime.datetime.now()
        timestamp = str(timestamp).replace(" ", "_")
        timestamp = timestamp.replace(":", "-")
        file = self.__audio_dir+timestamp+'.mp3'
        file_abs_path = str(Path(file).absolute())
        return file_abs_path
    
    def __wait_until_track_has_finished(self):
        while mixer.music.get_busy():
            time.sleep(0.1)
