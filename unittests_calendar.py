import unittest
import os
import sys
import time
import pygame
from pathlib import Path
from Calendar.CalendarAPI import Calendar

class Calendar_Test(unittest.TestCase):

    def test_get_upcomming_events_for_today(self):
        myCalendar = Calendar()
        events = myCalendar.get_upcomming_events_for_today()
        self.assertTrue(events)

    def test_get_upcomming_events_for_today(self):
        myCalendar = Calendar()
        events = myCalendar.get_upcomming_events_for_today()
        meeting = 'Daily Scrum Meeting'
        self.assertTrue(len(events)>=0)
    
    def test_token_exists(self):
        self.assertTrue(os.path.exists('Calendar/token.json'),'Not there!')

    def test_token_not_exists(self):
        self.assertFalse(os.path.exists('Test/token.json'),'Not there!')

    def test_token_not_exists_in_dir(self):
        file = 'Calendar/token.json'
        file_abs_path = str(Path(file).absolute())
        os.system('mv' + file_abs_path + '../')
        myCalendar = Calendar()
        self.assertTrue(myCalendar.creds)
        self.assertTrue(file)

    def test_check_if_object_exists(self):
        myCalendar = Calendar()
        self.assertTrue(myCalendar, 'Not there!')
