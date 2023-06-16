# -*- coding: utf-8 -*-
"""
Created on Wed Oct 27 11:29:47 2021

@author: leave
"""
import requests
import datetime
from collections import Counter, OrderedDict
#api=c38912e7a816d33583d81f8ab47af895
# documentation: https://openweathermap.org/api/one-call-api#data

class WeatherAPI:

    def __init__(self, lat, lon, api_key):
        self.lat = lat
        self.lon = lon
        self.api_url = "https://api.openweathermap.org/data/2.5/onecall?lat="+str(self.lat)+"&lon="+str(self.lon)+"&exclude=minutely,daily,alerts,current&units=metric&appid="+api_key
    

    def get_weather(self):
        response = requests.get(self.api_url)
        res_json=response.json()
        
        i=0
        weather=[]
        will_rain_sentence="Es wird regnen um etwa "
        will_rain=False
        currently_raining=False
        if res_json['hourly'][i]['weather'][0]['main']=="Rain":
            currently_raining=True
        
        while i<12:
            weather_description= res_json['hourly'][i]['weather'][0]['main']
            if weather_description=="Rain":
                will_rain=True
                ts = int(res_json['hourly'][i]['dt'])
                ts_readable=datetime.datetime.utcfromtimestamp(ts).strftime('%H:%M:%S')
                will_rain_sentence =will_rain_sentence + str(ts_readable)+" Uhr,"
                #print(will_rain)
            #print(weather_description)
            weather.append(weather_description)
            i=i+1
        if will_rain==False:
            will_rain_sentence="Kein Regen in den nächsten 12 Stunden"
        counts=Counter(weather)
        sorted_List_of_weather_descriptions = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
        sorted_dict_of_weather_descriptions=OrderedDict(sorted_List_of_weather_descriptions)
        main_weather_description = str(list(sorted_dict_of_weather_descriptions.keys())[0])
        #print(main_weather_description)
        
        #print(will_rain_sentence)
        main_weather_translation = self.translate_main_weather(main_weather_description)
        
        
        weather_answer={
            'currentTemp': res_json['hourly'][1]['temp'],
            'feelsLikeTempInCelsius': res_json['hourly'][1]['feels_like'],
            'humidity%': res_json['hourly'][1]['humidity'],
            'mainWeather': main_weather_description,
            'rain?': will_rain_sentence,
            'rainingAtTheMoment?': currently_raining,
            'mainWeatherTranslation': main_weather_translation
            }
        return weather_answer
    
    def translate_main_weather(self, main_weather_description):
        main_weather= main_weather_description
        translation="In den nächsten 12 Stunden wird es vor allem"
        #print(main_weather)
        #print(type(main_weather))
        if main_weather=="Thunderstorm":
            translation =translation +" gewittern."
        elif main_weather=="Drizzle":
            translation =translation +" Nieselregen geben. Nimm am besten eine Regenschirm mit."
        elif main_weather=="Rain":
            translation =translation +" regnen. Nimm am besten eine Regenschirm mit."
        elif main_weather=="Snow":
            translation =translation +" schneien. Zieh dich besser warm an."
        elif main_weather=="Mist":
            translation =translation +" nebelig sein."
        elif main_weather=="Smoke":
            translation =translation +" sehr viel Rauch in der Umgebung geben. Bleib am besten drinnen und lass Fenster und Türen geschlossen."
        elif main_weather=="Haze":
            translation =translation +" sehr dunstig und trüb."
        elif main_weather=="Dust":
            translation =translation +" sehr viel Staub in der Umgebung geben. Bleib am besten drinnen und lass Fenster und Türen geschlossen."
        elif main_weather=="Fog":
            translation =translation +" sehr starken Nebel geben."
        elif main_weather=="Sand":
            translation =translation +" sehr viel Sand in der Umgebung geben. Bleib am besten drinnen und lass Fenster und Türen geschlossen."
        elif main_weather=="Ash":
            translation =translation +" viel vulkanische Asche in deine Umgebung geben.Bleib am besten drinnen und lass Fenster und Türen geschlossen."
        elif main_weather=="Squall":
            translation =translation +" sehr windig. Zieh besser eine warme Jacke und eine Mütze auf."
        elif main_weather=="Tornado":
            translation =translation +" einen Tornado geben. Besser du bleibst heute innen."
        elif main_weather=="Clear":
            translation =translation +" einen klaren Himmel geben. Genieß die Sonne solange du kannst und mach vielleicht einen Spatziergang."
        elif main_weather=="Clouds":
            translation = translation +" bewölkt."
        else:
            translation="In den nächsten 12 Stunden wird es vor allem "+ str(main_weather)+"."
        #print(translation)
        return translation
    
   
    