import unittest

import os
import time
import pygame
from pathlib import Path

from stt.STT_Api import STT


class STT_Api_test(unittest.TestCase):

    def test_object_existence(self):
        mySTT = STT()
        self.assertTrue(
            mySTT,
            "API for STT could not be initialized."
        )
    
if __name__ == "__main__":
    unittest.main(module="STT_Api_test")
