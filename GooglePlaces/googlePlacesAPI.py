# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 09:58:31 2021

@author: leave
"""

import requests

class GooglePlacesAPI:
    
    def __init__(self, lat, lon, main_weather, api_key):
        self.lat = lat
        self.lon = lon
        self.main_weather= main_weather
        self.api_key= api_key
        self.base_api_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='+str(self.lat)+'%2C'+str(self.lon)+'&radius=10000'
        
    def get_nearby_places(self):
        
        places_good_weather=[['amusement_park', 'Vergnügungsparks'],['park', 'Parks'],['stadium', 'Stadien'],['zoo', 'Zoos']]
        places_bad_weather=[['aquarium', 'Aquarien'], ['art_gallery', 'Kunstgalerien'],['bar','Bars'],['bowling_alley','Bowling'],
                            ['cafe','Cafés'],['casino','Casinos'],['gym','Gyms'],['library','Büchereien'],
                            ['meal_takeaway','Essen zum abholen'],['movie_theater','Kinos'],['museum','Museen'],['night_club','Nachtclubs'],
                            ['restaurant','Restaurants'],['shopping_mall','Einkaufszentren'],['spa','Spas'],['tourist_attraction','Touristattraktionen']]
        
        results=[]
        all_names=[]
        error=""
        
        places_dict_eng = {
            'amusement_park':0,
            'park':0,
            'stadium':0,
            'zoo':0,
            'aquarium':0,
            'art_gallery':0,
            'bar':0,
            'bowling_alley':0,
            'cafe':0,
            'casino':0,
            'gym':0,
            'library':0,
            'meal_takeaway':0,
            'movie_theater':0,
            'museum':0,
            'night_club':0,
            'restaurant':0,
            'shopping_mall':0,
            'spa':0,
            'tourist_attraction':0
            }
        
        if self.main_weather=='Clear' or self.main_weather=='Clouds':
            for element in places_good_weather:
                #print(element[0], element[1])
                api_url=self.base_api_url + '&type='+str(element[0])+'&key='+self.api_key
                #print(api_url)
                response=requests.get(api_url)
                res_json=response.json()
                
                if res_json['status']=="OK":
                    #print(str(element[1]), len(res_json))
                    places_dict_eng[element[0]]= len(res_json['results'])
                    i=0
                    while i<len(res_json['results']):
                        place={'name': res_json['results'][i]['name'],
                               'location': res_json['results'][i]['geometry']['location'],
                               'type': [element[1]]}
                        #print("hallo")
                        #print(place)
                        try:
                            open_now=res_json['results'][i]['opening_hours']['open_now']
                        except:
                            open_now=True
                        if open_now==True:
                            
                            if res_json['results'][i]['name'] not in all_names:
                                results.append(place)
                                all_names.append(res_json['results'][i]['name'])
                            else:
                                for places in results:
                                    if res_json['results'][i]['name'] == places['name']:
                                        places['type'].append(element[1])
                        else:
                            places_dict_eng[element[0]]= places_dict_eng[element[0]]-1
                        i=i+1
                else:
                    error ="Invalide API Anfrage. Möglicherweise gibt es Probleme mit dem API Key oder der Positionsangabe."
                
                
                                               
                
            for element in places_bad_weather:
                #print(element[0], element[1])
                api_url=self.base_api_url + '&type='+str(element[0])+'&key='+self.api_key
                #print(api_url)
                response=requests.get(api_url)
                res_json=response.json()
                i=0
                if res_json['status']=="OK":
                    #print(str(element[1]), len(res_json['results']))
                    places_dict_eng[element[0]]= len(res_json['results'])
                    
                    while i<len(res_json['results']):
                        place={'name': res_json['results'][i]['name'],
                               'location': res_json['results'][i]['geometry']['location'],
                               'type': [element[1]]}
                        
                        #print(place)
                        try:
                            open_now=res_json['results'][i]['opening_hours']['open_now']
                        except:
                            open_now=True
                        if open_now==True:
                            
                            if res_json['results'][i]['name'] not in all_names:
                                results.append(place)
                                all_names.append(res_json['results'][i]['name'])
                            else:
                                for places in results:
                                    if res_json['results'][i]['name'] == places['name']:
                                        places['type'].append(element[1])
                        else:
                            places_dict_eng[element[0]]= places_dict_eng[element[0]]-1 
                        i=i+1
                else:
                    error ="Invalide API Anfrage. Möglicherweise gibt es Probleme mit dem API Key oder der Positionsangabe."
                
                
                
        else:
            for element in places_bad_weather:
                #print(element[0], element[1])
                api_url=self.base_api_url + '&type='+str(element[0])+'&key='+self.api_key
                #print(api_url)
                response=requests.get(api_url)
                res_json=response.json()
                i=0
                if res_json['status']=="OK":
                    #print(str(element[1]), len(res_json))
                    places_dict_eng[element[0]]= len(res_json['results'])
                    
                    while i<len(res_json['results']):
                        place={'name': res_json['results'][i]['name'],
                               'location': res_json['results'][i]['geometry']['location'],
                               'type': [element[1]]}
                        
                        try:
                            open_now=res_json['results'][i]['opening_hours']['open_now']
                        except:
                            open_now=True
                        if open_now==True:
                            
                            if res_json['results'][i]['name'] not in all_names:
                                results.append(place)
                                all_names.append(res_json['results'][i]['name'])
                            else:
                                for places in results:
                                    if res_json['results'][i]['name'] == places['name']:
                                        places['type'].append(element[1])
                        else:
                            places_dict_eng[element[0]]= places_dict_eng[element[0]]-1
                        i=i+1
                else:
                    error ="Invalide API Anfrage. Möglicherweise gibt es Probleme mit dem API Key oder der Positionsangabe."
                
        
        #print(places_dict_eng)
        places_de = {
            'Vergnügungsparks':places_dict_eng['amusement_park'],
            'Parks':places_dict_eng['park'],
            'Stadien':places_dict_eng['stadium'],
            'Zoos':places_dict_eng['zoo'],
            'Aquarien':places_dict_eng['aquarium'],
            'Kunstgalerien':places_dict_eng['art_gallery'],
            'Bars':places_dict_eng['bar'],
            'Bowling':places_dict_eng['bowling_alley'],
            'Cafés':places_dict_eng['cafe'],
            'Casinos':places_dict_eng['casino'],
            'Gyms':places_dict_eng['gym'],
            'Büchereien':places_dict_eng['library'],
            'Essen zum abholen':places_dict_eng['meal_takeaway'],
            'Kinos':places_dict_eng['movie_theater'],
            'Museen':places_dict_eng['museum'],
            'Nachtclubs':places_dict_eng['night_club'],
            'Restaurants':places_dict_eng['restaurant'],
            'Einkaufszentren':places_dict_eng['shopping_mall'],
            'Spas':places_dict_eng['spa'],
            'Touristattraktionen':places_dict_eng['tourist_attraction']
        }
        #print(places_de)
        places_de = {k:v for k,v in places_de.items() if v != 0}
        #print(places_de)
        
        return results, places_de, places_dict_eng, error