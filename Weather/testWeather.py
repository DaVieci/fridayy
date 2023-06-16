# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 18:58:53 2021

@author: leave
"""
import geocoder
from weatherAPI import WeatherAPI
g = geocoder.ip('me')
lat=g.latlng[0]
lon=g.latlng[1]
print("lat: "+str(lat))
print("lon: "+str(lon))
w = WeatherAPI(lat, lon, "key")
res=w.get_weather()
print(res)
print(res['rain?'])