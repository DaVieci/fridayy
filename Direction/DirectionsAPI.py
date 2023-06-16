import requests
import urllib.request
import json
import googlemaps
from datetime import datetime, timedelta
import webbrowser


class DirectionsApi:
    
  def __init__(self, api_key):
    self.adress_valid = True
    self.__key = api_key
    self.__curr_lat = 0
    self.__curr_lon = 0
    self.__dest_lat = 0
    self.__dest_lon = 0
    self.__endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
    self.__maps_url = "https://www.google.com/maps/dir/?api=1&origin="
  
  def set_current_position(self, lat, lon):
    self.__curr_lat = lat
    self.__curr_lon = lon

  def set_destination_position_adress(self, adress):
    gmaps = googlemaps.Client(key=self.__key)
    geocode_dest = gmaps.geocode(adress)
    self.__dest_lat = geocode_dest[0]["geometry"]["location"]["lat"]
    self.__dest_lon = geocode_dest[0]["geometry"]["location"]["lng"]
    print(self.__dest_lat, self.__dest_lon)

  def set_destination_position_lat_lon(self, lat, lon):
    self.__dest_lat = lat
    self.__dest_lon = lon

  def translate_travelmode (self, travelmode):
      travelmode = travelmode.lower()
      if 'auto' in travelmode:
          travelmode = 'driving'
      elif 'laufen' in travelmode:
          travelmode = 'walking'
      elif 'fahrrad' in travelmode:
          travelmode = 'bicycling'
      elif 'bus'in travelmode or 'bahn' in travelmode or 'zug' in travelmode:
          travelmode = 'transit'
      return travelmode

  def route_to_destination(self, travelmode):
    if self.adress_valid:
      url = self.__maps_url + str(self.__curr_lat)+ "," + str(self.__curr_lon)+ "&destination="+ str(self.__dest_lat) +"," + str(self.__dest_lon) + "&travelmode="+ travelmode
      self.open_url_in_browser(url)
    else:
      self.adress_valid = True
  
  def open_url_in_browser(self, url):
    webbrowser.open(url)
    print(url)

  def say_direction_info(self, travelmode): 
    nav_request = 'origin={}&destination={}&mode={}&key={}'.format(str(self.__curr_lat) + ","+ str(self.__curr_lon),str(self.__dest_lat) + ","+ str(self.__dest_lon),travelmode, self.__key)
    request= self.__endpoint + nav_request
    response = urllib.request.urlopen(request).read()
    directions = json.loads(response)

    direction_text = ""
    try:
      self.adress_valid = True
      routes = directions['routes']
      polyline = routes[0]['overview_polyline']['points']
      legs = routes[0]['legs']
      summary = routes[0]['summary']
      print(summary)
      steps = legs[0]['steps']
      distance = legs[0]['distance']['text']
      duration = legs[0]['duration']['text']
      direction_text = "Dein Ziel ist " + duration + " und " + distance + " entfernt."
    except:
      self.adress_valid = False
      direction_text = "Invalide Adresse!"
    return direction_text