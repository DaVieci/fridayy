# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 08:46:28 2021

@author: leave
"""
import requests
import json
import geocoder
from geopy.geocoders import Nominatim


class Location:

  def __init__(self, api_key):
    self.__key = api_key
    self.__lat = 0
    self.__lon = 0
    self.set_new_locator()
    self.set_new_position()
  
  def set_new_locator(self):
    self.g = geocoder.ip('me')
    self.geolocator = Nominatim(user_agent="geoapiExercises")
  
  def set_new_position(self):
    locationurl= 'https://www.googleapis.com/geolocation/v1/geolocate?key='
    locrequest = locationurl + self.__key
    loc = requests.post(locrequest)
    json_response = json.loads(loc.text)
    self.__lat = json_response['location']['lat']
    self.__lon = json_response['location']['lng']
  
  def get_latitude(self):
    lat = self.__lat
    return lat
  
  def get_longitude(self):
    lon = self.__lon
    return lon
  
  def get_current_address(self):
    location = self.geolocator.reverse(str(self.__lat)+","+str(self.__lon))
    address = location.raw['address']
    return address
