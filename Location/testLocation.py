# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 17:02:00 2021

@author: leave
"""

import geocoder
from location import Location
g = geocoder.ip('me')
lat=g.latlng[0]
lon=g.latlng[1]
print("lat: "+str(lat))
print("lon: "+str(lon))
w = Location()
res=w.get_city()
print(res)