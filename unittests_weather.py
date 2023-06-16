# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 17:31:21 2021

@author: leave
"""

import unittest

from Database.sqliteAPI import Datenbank
from Weather.weatherAPI import WeatherAPI

class test_weather_methods(unittest.TestCase):
    
    def __init__(self, *args, **kwargs):
        super(test_weather_methods, self).__init__(*args, **kwargs)
        self.myDB = Datenbank()
        keys = self.myDB.getKeys()
        self.__weather_key = keys[0]['weather_key']
        self.test_lat = 48.2752
        self.test_lon = 8.8546
        self.myWeather = WeatherAPI(self.test_lat, self.test_lon, self.__weather_key)
       
        
    def test_get_weather_valid_input(self):
        weather = self.myWeather.get_weather()
        self.assertEqual(len(weather), 7)
        
    def test_get_weather_wrong_key(self):
        myWeather_invalid = WeatherAPI(self.test_lat, self.test_lon, "wrongKey")
        with self.assertRaises(KeyError):
           weather = myWeather_invalid.get_weather()
           
    def test_initiaize_missing_param_lat(self):
        with self.assertRaises(TypeError):
           WeatherAPI(self.test_lon, self.__weather_key)
           
    def test_initiaize_missing_param_key(self):
        with self.assertRaises(TypeError):
           WeatherAPI(self.test_lat, self.test_lon)
           
    def test_translate_main_weather_valid_thunderstorm(self):
        weather = self.myWeather.translate_main_weather("Thunderstorm")
        self.assertEqual(weather, "In den nächsten 12 Stunden wird es vor allem gewittern.")
        
    def test_translate_main_weather_valid_drizzle(self):
        weather = self.myWeather.translate_main_weather("Drizzle")
        self.assertEqual(weather, "In den nächsten 12 Stunden wird es vor allem Nieselregen geben. Nimm am besten eine Regenschirm mit.")
        
    def test_translate_main_weather_valid_rain(self):
        weather = self.myWeather.translate_main_weather("Rain")
        self.assertEqual(weather, "In den nächsten 12 Stunden wird es vor allem regnen. Nimm am besten eine Regenschirm mit.")
        
    def test_translate_main_weather_valid_snow(self):
        weather = self.myWeather.translate_main_weather("Snow")
        self.assertEqual(weather, "In den nächsten 12 Stunden wird es vor allem schneien. Zieh dich besser warm an.")
        
    def test_translate_main_weather_valid_mist(self):
        weather = self.myWeather.translate_main_weather("Mist")
        self.assertEqual(weather, "In den nächsten 12 Stunden wird es vor allem nebelig sein.")
        
    def test_translate_main_weather_valid_smoke(self):
        weather = self.myWeather.translate_main_weather("Smoke")
        self.assertEqual(weather, "In den nächsten 12 Stunden wird es vor allem sehr viel Rauch in der Umgebung geben. Bleib am besten drinnen und lass Fenster und Türen geschlossen.")
        
    def test_translate_main_weather_valid_haze(self):
        weather = self.myWeather.translate_main_weather("Haze")
        self.assertEqual(weather, "In den nächsten 12 Stunden wird es vor allem sehr dunstig und trüb.")
        
    def test_translate_main_weather_valid_dust(self):
        weather = self.myWeather.translate_main_weather("Dust")
        self.assertEqual(weather, "In den nächsten 12 Stunden wird es vor allem sehr viel Staub in der Umgebung geben. Bleib am besten drinnen und lass Fenster und Türen geschlossen.")
        
    def test_translate_main_weather_valid_fog(self):
        weather = self.myWeather.translate_main_weather("Fog")
        self.assertEqual(weather, "In den nächsten 12 Stunden wird es vor allem sehr starken Nebel geben.")
        
    def test_translate_main_weather_valid_sand(self):
        weather = self.myWeather.translate_main_weather("Sand")
        self.assertEqual(weather, "In den nächsten 12 Stunden wird es vor allem sehr viel Sand in der Umgebung geben. Bleib am besten drinnen und lass Fenster und Türen geschlossen.")
        
    def test_translate_main_weather_valid_ash(self):
        weather = self.myWeather.translate_main_weather("Ash")
        self.assertEqual(weather, "In den nächsten 12 Stunden wird es vor allem viel vulkanische Asche in deine Umgebung geben.Bleib am besten drinnen und lass Fenster und Türen geschlossen.")
        
    def test_translate_main_weather_valid_squall(self):
        weather = self.myWeather.translate_main_weather("Squall")
        self.assertEqual(weather, "In den nächsten 12 Stunden wird es vor allem sehr windig. Zieh besser eine warme Jacke und eine Mütze auf.")
        
    def test_translate_main_weather_valid_tornado(self):
        weather = self.myWeather.translate_main_weather("Tornado")
        self.assertEqual(weather, "In den nächsten 12 Stunden wird es vor allem einen Tornado geben. Besser du bleibst heute innen.")
        
    def test_translate_main_weather_valid_clear(self):
        weather = self.myWeather.translate_main_weather("Clear")
        self.assertEqual(weather, "In den nächsten 12 Stunden wird es vor allem einen klaren Himmel geben. Genieß die Sonne solange du kannst und mach vielleicht einen Spatziergang.")
        
    def test_translate_main_weather_valid_clouds(self):
        weather = self.myWeather.translate_main_weather("Clouds")
        self.assertEqual(weather, "In den nächsten 12 Stunden wird es vor allem bewölkt.")
        
    def test_translate_main_weather_missing_param(self):
        with self.assertRaises(TypeError):
            weather = self.myWeather.translate_main_weather()
            
    def test_translate_main_weather_wrong_mainWeather(self):
        weather = self.myWeather.translate_main_weather("wolkig mit Aussicht auf Fleischbällchen")
        self.assertEqual(weather, "In den nächsten 12 Stunden wird es vor allem wolkig mit Aussicht auf Fleischbällchen.")
        
