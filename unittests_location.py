# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 18:03:29 2021

@author: leave
"""

import unittest

from Database.sqliteAPI import Datenbank
from Location.location import Location

class test_location_methods(unittest.TestCase):
    
    def __init__(self, *args, **kwargs):
        super(test_location_methods, self).__init__(*args, **kwargs)
        self.myDB = Datenbank()
        keys = self.myDB.getKeys()
        self.__directions_key = keys[0]['directions_key']
        self.test_lat = 48.2752
        self.test_lon = 8.8546
        self.myLocation = Location(self.__directions_key)
        
    def test_initiaize_missing_param_key(self):
        with self.assertRaises(TypeError):
           Location()
           
    def test_initiaize_wrong_key(self):
        with self.assertRaises(KeyError):
           Location("wrongKey")
          
    def test_set_new_locator(self):
        self.assertEqual(None, self.myLocation.set_new_locator())
        
    def test_set_new_position(self):
        self.assertEqual(None, self.myLocation.set_new_position())
        
    def test_get_latitude(self):
        self.assertEqual(float, type(self.myLocation.get_latitude()))
        
    def test_get_longitude(self):
        self.assertEqual(float, type(self.myLocation.get_longitude()))
        
    def test_get_current_address(self):
        address = self.myLocation.get_current_address()
        self.assertTrue(len(address)== 8 or len(address)== 9)
           
           
           
