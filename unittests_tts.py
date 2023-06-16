import unittest

import os
import time
import pygame
from pathlib import Path

from tts.TTS_Api import TTS


class TTS_Api_test(unittest.TestCase):

    def test_object_existence(self):
        myTTS = TTS()
        self.assertTrue(
            myTTS,
            "API for TTS could not be initialized."
        )

    def test_output_of_valid_text(self):
        myTTS = TTS()
        text = "Hallo, ich bin Friday."
        file = myTTS.get_speech_file_from_text(text)
        self.assertTrue(
            file,
            "File could not be created or does not exist."
        )
        os.system("rm "+file)
    
    def test_output_of_valid_file_type(self):
        myTTS = TTS()
        text = "Hallo, ich bin Friday."
        file = myTTS.get_speech_file_from_text(text)
        self.assertIn('.mp3', file)
        os.system("rm "+file)
    
    def test_output_of_valid_audio_feedback(self):
        myTTS = TTS()
        text = "Die Wiedergabe dieses Textes muss mindestens 5 Sekunden dauern."
        file = myTTS.get_speech_file_from_text(text)
        time_start = time.time()
        myTTS.play_speech_file(file)
        time_end = time.time()
        elapsed_time = time_end - time_start
        self.assertGreater(elapsed_time, 5)
        os.system("rm "+file)
    
    def test_output_of_empty_text(self):
        myTTS = TTS()
        text = " "
        with self.assertRaises(AssertionError):
            file = myTTS.get_speech_file_from_text(text)
            os.system("rm "+file)
    
    def test_output_of_non_existing_file(self):
        myTTS = TTS()
        file = str(Path("doesnt_exist.mp3").absolute())
        with self.assertRaises(pygame.error):
            myTTS.play_speech_file(file)
    
    def test_output_of_invalid_audio_file(self):
        myTTS = TTS()
        file = str(Path("not_an_audio_file.txt").absolute())
        f = open(file, "w")
        f.write("This is a txt file!")
        f.close()
        with self.assertRaises(pygame.error):
            myTTS.play_speech_file(file)
        os.system("rm "+file)
    

if __name__ == "__main__":
    unittest.main(module="TTS_Api_test")
