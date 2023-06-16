# -*- coding: utf-8 -*-
"""
Created on Sun Nov  7 15:14:33 2021

@author: leave
"""

from googlePlacesAPI import GooglePlacesAPI
import pprint

import geocoder
g = geocoder.ip('me')

places = GooglePlacesAPI(g.latlng[0],g.latlng[1], 'Clear', "")

res = places.get_nearby_places()
#print(res)
pprint.pprint(res[1])
#print(len(res[0]))

#https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=48.858093%2C2.294694&type=zoo&key=
#https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=48.858093%2C2.294694&type=zoo&rankby=distance&key=