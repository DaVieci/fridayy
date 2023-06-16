# -*- coding: utf-8 -*-
"""
Created on Sat Nov 27 13:49:49 2021

@author: leave
"""

import unittest

from Database.sqliteAPI import Datenbank
from GooglePlaces.googlePlacesAPI import GooglePlacesAPI

class test_places_methods(unittest.TestCase):
    
    def __init__(self, *args, **kwargs):
        super(test_places_methods, self).__init__(*args, **kwargs)
        self.myDB = Datenbank()
        keys = self.myDB.getKeys()
        self.__places_key = keys[0]['places_key']
        self.test_lat = 48.2752
        self.test_lon = 8.8546
        self.myPlaces = GooglePlacesAPI(self.test_lat, self.test_lon, "Clear", self.__places_key)
        
    def test_initiaize_missing_param_key(self):
        with self.assertRaises(TypeError):
           GooglePlacesAPI(self.test_lat, self.test_lon, "Clear")
           
    def test_get_nearby_places_wrong_key(self):
        myPlaces_invalid = GooglePlacesAPI(self.test_lat, self.test_lon, "Clear", "wrongKey")
        places= myPlaces_invalid.get_nearby_places()
        self.assertTrue("Invalide API Anfrage" in places[3])
        
    def test_get_nearby_places_wrong_type_of_lat_lon(self):
        myPlaces_invalid = GooglePlacesAPI("self.test_lat", "self.test_lon", "Clear", "wrongKey")
        places= myPlaces_invalid.get_nearby_places()
        self.assertTrue("Invalide API Anfrage" in places[3])
           
    def test__get_nearby_places_valid_good_weather(self):
        places= self.myPlaces.get_nearby_places()
        self.assertEqual(len(places),4)
        
    def test__get_nearby_places_valid_types_de_good_weather(self):
        places= self.myPlaces.get_nearby_places()
        self.assertTrue(len(places[1]) <=20)
        
    def test__get_nearby_places_valid_types_eng_good_weather(self):
        places= self.myPlaces.get_nearby_places()
        self.assertTrue(len(places[2]) <=20)
           
    def test__get_nearby_places_valid_bad_weather(self):
        myPlaces_bad_weather = GooglePlacesAPI(self.test_lat, self.test_lon, "Rain", self.__places_key)
        places= myPlaces_bad_weather.get_nearby_places()
        self.assertEqual(len(places),4)
        
    def test__get_nearby_places_valid_types_de_bad_weather(self):
        myPlaces_bad_weather = GooglePlacesAPI(self.test_lat, self.test_lon, "Rain", self.__places_key)
        places= myPlaces_bad_weather.get_nearby_places()
        self.assertTrue(len(places[1]) <=20)
        
    def test__get_nearby_places_valid_types_eng_bad_weather(self):
        myPlaces_bad_weather = GooglePlacesAPI(self.test_lat, self.test_lon, "Rain", self.__places_key)
        places= myPlaces_bad_weather.get_nearby_places()
        self.assertTrue(len(places[2]) <=20)
        


