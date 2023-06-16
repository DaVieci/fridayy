#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import time
import random
import webbrowser
import _thread
from datetime import datetime
from datetime import timedelta
import zahlwort2num as w2n

from tts.TTS_Api import TTS
from stt.STT_Api import STT
from spotify.SpotifyHtmlScraper import SpotifyCharts
from Calendar.CalendarAPI import Calendar

from Database.sqliteAPI import Datenbank
from Weather.weatherAPI import WeatherAPI
from GooglePlaces.googlePlacesAPI import GooglePlacesAPI
from Location.location import Location
from Direction.DirectionsAPI import DirectionsApi

import pprint



class Agent:
    
    def __init__(self):
        self.initialize_apis()
        self.greet_user()
        self.start_agent()
    
    def initialize_apis(self):
        print("Initialisiere APIs...")

        self.myTTS = TTS()
        self.mySTT = STT()

        self.myDB = Datenbank()
        keys = self.myDB.getKeys()
        self.__weather_key = keys[0]['weather_key']
        self.__places_key = keys[0]['places_key']
        self.__directions_key = keys[0]['directions_key']
        
        self.myLocation = Location(self.__directions_key)
        self.lat = self.myLocation.get_latitude()
        self.lon = self.myLocation.get_longitude()
        self.current_location = self.myLocation.get_current_address()
        
        self.myCalendar = Calendar()

        self.myDirections = DirectionsApi(self.__directions_key)
       
        self.myPlayer = SpotifyCharts()
        country_code = self.current_location['country_code']
        # -------- playlist based on another country -------------
        #country_code = 'kr'
        self.myPlayer.set_charts_list_by_country(country_code)
        
        self.myWeather = WeatherAPI(self.lat, self.lon, self.__weather_key)
        self.current_weather = self.myWeather.get_weather()
        
        self.myPlaces = GooglePlacesAPI(self.lat, self.lon, self.current_weather['mainWeather'], self.__places_key)

        
    def greet_user(self):
        greeting="Hallo, ich bin Friday. Mit wem habe ich das Vergnügen?"
        self.speak_text(greeting)
        name=input("Name:").strip()

        exists = self.myDB.checkIfUserExists(name)
        if exists:
            speech="Hallo "+ name +"! Schön Dich wiederzusehen."
            self.speak_text(speech)
        else:
            speech="Hallo "+ name +"! Ich glaube wir hatten noch nicht das Vergnügen. "
            speech=speech+"Bitte gib mir ein paar Informationen über Dich, damit ich Dir am besten assistieren kann."
            self.speak_text(speech)
            
            speech="Bitte gib Deine E-Mail-Adresse an."
            self.speak_text(speech)
            email=input("E-Mail:").strip()
            
            #speech="Um für Dich auf Spotify zuzugreifen, benötige ich Deine Client-ID."
            #self.speak_text(speech)
            #clientID=input("clientID:")
            clientID="d25f8000cd74459b83e4439fe3a8f6f4"
            
            #speech="Außerdem benötige ich dafür noch deine Secret-ID."
            #self.speak_text(speech)
            #secretID=input("secretID:")
            secretID="80d71854149e43b7999451c42efdf5ed"
            
            speech="Was sind Deine Hobbies?"
            self.speak_text(speech)
            hobbies=input("Hobbies:").strip()
            
            speech="Welches Transportmittel benutzt Du am liebsten?"
            self.speak_text(speech)
            transport=input("Transportmittel:").strip()
            
            speech="Bitte gib drei Uhrzeiten ein, zu denen du Musik hören möchtest."
            self.speak_text(speech)
            sp_times=input("Uhrzeiten im Format hh:mm:ss,hh:mm:ss,hh:mm:ss:")
            
            speech="Das wäre schon alles. Bitte gib mir kurz Zeit das zu verarbeiten."
            self.speak_text(speech)
            preferences={
                "name":name,
                "email":email,
                "clientID":clientID,
                "secretID":secretID,
                "hobby":hobbies,
                "transportation":transport,
                "location": str(self.lat)+","+str(self.lon),
                "sp_time": sp_times
            }
            print("Präferenzen:", preferences)
            self.myDB.insertIntoTablePreferences(preferences)
        self.initialize_user_data(name)
        self.play_welcome_message()

    def initialize_user_data(self, userName):
        preferences = self.myDB.getPreferencesForUser(userName)
        
        print("Initialisiere User Daten...")
        self.__name = preferences[0]['name']
        self.__transportation = preferences[0]['transportation']
        hobbies = preferences[0]['hobby']
        self.__hobby_split = hobbies.split(', ')
        
        self.__time = ":".join(str(datetime.now()).split(" ")[1].split(":")[:2])
        self.__date = str(datetime.now()).split(" ")[0]
        try:
            self.__town = self.current_location['city']
        except:
            self.__town = self.current_location['town']
        self.__country = self.current_location['country']
        self.__temperature = str(self.current_weather['currentTemp'])+" Grad"
        self.__weather = self.current_weather['mainWeatherTranslation']
        self.__meetings = self.myCalendar.get_upcomming_events_for_today()
        self.__meeting_remindered = self.create_reminder_list(len(self.__meetings))
        self.__playlist = self.myPlayer.get_charts_list()
        self.__music_time = preferences[0]['sp_time'].split(',')
        # ------- Test music player with custom time ----------
        #self.__music_time = ['12:34:00','23:00:00','23:30:00']
        print(self.__music_time)

    def create_reminder_list(self, length):
        reminder_list = []
        for i in range(0, length):
            reminder_list.append(False)
        return reminder_list    

    def play_welcome_message(self):
        msg_user_and_time = "Hallo "+self.__name+". Wir haben "+self.__time+" Uhr. "
        msg_weather_and_location = self.get_weather_text()
        msg_meetings = "Du hast heute "+str(len(self.__meetings))+" Meetings. "
        welcome_msg = msg_user_and_time+msg_weather_and_location+msg_meetings
        self.speak_text(welcome_msg)
        if len(self.__meetings)==0:
            self.propose_free_time_activity(0)
    
    def speak_text(self, text):
        audio_file = self.myTTS.get_speech_file_from_text(text)
        print(text)
        self.myTTS.play_speech_file(audio_file)
    
    def start_agent(self):
        print("Starte Agent...\n")
        print("Drücke '⏎', um mit Agenten zu sprechen.\n")
        self.communicator_active = False
        self.locker = _thread.allocate_lock()
        try:
            _thread.start_new_thread(self.handle_meeting_reminders, ("Meeting-Thread", 1))
            _thread.start_new_thread(self.handle_music_player, ("Music-Thread", 1))
            _thread.start_new_thread(self.handle_location_checker, ("Location-Thread", 10))
            _thread.start_new_thread(self.handle_speech_communicator, ("Speech-Thread", 1))
            _thread.start_new_thread(self.handle_activity_suggestion, ("FreeTime-Thread", 1))
        except:
            print("Error: Threads could not be started")
        while 1:
            time.sleep(1)
            pass
    
    def handle_meeting_reminders(self, thread_name, thread_delay):
        print("START", thread_name)
        while True:
            if not self.locker.locked():
                current_time = datetime.now()
                self.check_time_for_meetings(current_time)
            time.sleep(thread_delay)

    def handle_music_player(self, thread_name, thread_delay):
        print("START", thread_name)
        while True:
            if not self.locker.locked():
                current_time = datetime.now()
                self.check_time_for_music(current_time)
            time.sleep(thread_delay)
    
    def handle_location_checker(self, thread_name, thread_delay):
        print("START", thread_name)
        while True:
            if not self.locker.locked():
                self.locker.acquire()
                self.myLocation = Location(self.__directions_key)
                self.lat = self.myLocation.get_latitude()
                self.lon = self.myLocation.get_longitude()
                self.current_location = self.myLocation.get_current_address()
                new_location=str(self.lat)+","+str(self.lon)
                self.myDB.updateLocation(new_location, self.__name)
                self.locker.release()
            time.sleep(thread_delay)
    
    def handle_speech_communicator(self, thread_name, thread_delay):
        print("START", thread_name)
        while True:
            self.detect_input()
            if self.communicator_active:
                self.start_communication_with_agent()
                self.communicator_active = False
                self.locker.release()
            time.sleep(thread_delay)
    
    def handle_activity_suggestion(self, thread_name, thread_delay):
        print("START", thread_name)
        while True:
            if not self.locker.locked():
                current_time = datetime.now()
                self.check_time_for_activities(current_time)
            time.sleep(thread_delay)
    
    def check_time_for_meetings(self, current_time):
        if len(self.__meetings) > 0:
            i = 0
            while self.__meeting_remindered[i] and i<len(self.__meetings)-1:
                i = i + 1
            if not self.__meeting_remindered[i]:
                m = self.__meetings[i]
                meeting_date_time = m['start']
                meeting_date_time = meeting_date_time.split("+")[0]
                meeting_date_time = " ".join(meeting_date_time.split("T"))
                meeting_time = datetime.strptime(meeting_date_time, '%Y-%m-%d %H:%M:%S')
                d = current_time + timedelta(minutes=15)
                time_remaining = meeting_time - d
                if time_remaining.total_seconds() <= 0:
                    self.locker.acquire()
                    time_remaining = meeting_time - current_time
                    if time_remaining.total_seconds() <= 0:
                        text = "\nMeeting gestartet: "
                    else:
                        text = "\nMeeting in 15 Minuten: "
                    text = text + m['titel']+" an dem Ort "+m['location']+". "
                    self.speak_text(text)
                    self.__meeting_remindered[i] = True
                    self.show_directions(m['location'])
                    self.locker.release()
                    print("\n🔊⏎")

    def show_directions(self, adress):
        self.myDirections.set_current_position(self.myLocation.get_latitude(),self.myLocation.get_longitude())
        self.myDirections.set_destination_position_adress(adress)
        travelmode = self.myDirections.translate_travelmode(self.__transportation)
        text = self.myDirections.say_direction_info(travelmode)
        self.speak_text(text)
        self.myDirections.route_to_destination(travelmode)

    def check_time_for_music(self, current_time):
        for e in self.__music_time:
            upcoming_sp_time = self.__date+' '+e
            music_time = datetime.strptime(upcoming_sp_time, '%Y-%m-%d %H:%M:%S')
            time_remaining = music_time - current_time
            if -10<=time_remaining.total_seconds() and time_remaining.total_seconds()<=0:
                self.locker.acquire()
                n = self.get_random_number_from_playlist()
                t = self.__playlist[n]
                text = "\nEs ist Zeit für entspannte Musik. "
                text = text + "Ich habe ein populäres Lied aus der Region ausgesucht: "
                text = text + t[1]+" von "+t[2]+"."
                self.speak_text(text)
                track_url = t[3]
                webbrowser.open(track_url)
                self.locker.release()
                print("\n🔊⏎")
    
    def detect_input(self):
        while True:
            user_input = input("\n🔊⏎\n")
            if not self.locker.locked():
                if user_input == "":
                    self.locker.acquire()
                    self.communicator_active = True
                    break
            time.sleep(0.1)
    
    def get_random_number_from_playlist(self):
        max_number = len(self.__playlist)-1
        rand_number = random.randint(0, max_number)
        return rand_number
    
    def start_communication_with_agent(self):
        print("Ja bitte?")
        self.mySTT.start_mic_listening()
        recognized_text = self.mySTT.get_text_from_recognized_speech()
        if recognized_text == -1:
            error_msg = "Tut mir Leid, ich konnte das nicht verstehen."
            self.speak_text(error_msg)
        else:
            print("-\""+recognized_text+"\"")
            self.analyze_spoken_text(recognized_text.lower())
    
    def analyze_spoken_text(self, text):
        if "wie geht" in text:
            answer_text = "Hallo "+self.__name+". Mir geht es gut. Wie kann ich Dir weiterhelfen?"
            self.speak_text(answer_text)
        elif "meeting" in text:
            answer_text = self.get_meetings_text()
            self.speak_text(answer_text)
        elif "musik" in text or "lied" in text or "spotify" in text:
            n = self.get_random_number_from_playlist()
            t = self.__playlist[n]
            answer_text = "Ich habe ein populäres Lied aus der Region ausgesucht: "
            answer_text = answer_text + t[1]+" von "+t[2]+"."
            self.speak_text(answer_text)
            track_url = t[3]
            webbrowser.open(track_url)
        elif "wetter" in text or "grad" in text:
            answer_text = self.get_weather_text()
            self.speak_text(answer_text)
        elif "standort" in text or "wo bin ich" in text or "welcher stadt" in text:
            answer_text = self.get_location_text()
            self.speak_text(answer_text)
        elif "wo bist du" in text:
            answer_text = "Ich bin über all"
            self.speak_text(answer_text)
        elif "danke" in text:
            answer_text = "Gern geschehen."
            self.speak_text(answer_text)
        elif "nähe" in text:
            self.propose_place()
        elif "ziel" in text:
            answer_text = "Wohin möchtest du?"
            self.speak_text(answer_text)
            self.mySTT.start_mic_listening()
            recognized_text = self.mySTT.get_text_from_recognized_speech()
            if recognized_text == -1:
                error_msg = "Tut mir Leid, ich konnte das nicht verstehen."
                self.speak_text(error_msg)
            else:
                print("-\""+recognized_text+"\"")
                self.show_directions(recognized_text)
        elif "user" in text:
            self.greet_user() 
        elif ("aquarien" in text or "bars" in text or "bowling" in text or 
              "bücherei" in text or "cafés" in text or "casinos" in text or 
              "einkaufszentren" in text or "essen zum abholen" in text or 
              "gyms" in text or "kinos" in text or "kunstgalerien" in text or 
              "museen" in text or "nachtclubs" in text or "parks" in text or 
              "Vergnügungsparks" or "restaurants" in text or "spas" in text or 
              "stadien" in text or "touristattraktionen" in text or "zoos" in text):
            answer_text="Einen Moment bitte, ich suche."
            self.speak_text(answer_text)
            self.get_places()
            answer_text="Ich habe die folgenden Orte gefunden:"
            self.speak_text(answer_text)
            already_printed=[]
            self.__proposed = []
            proposed_index = 1
            #pprint.pprint(self.__types)
            for key in self.__types:
                #print(key)
                if key.lower() in text:
                    #print(key.lower())
                    i=0
                    while i<len(self.__places):
                        #print(i, self.__places[i]['type'])
                        if key in self.__places[i]['type']:
                            #print(self.__places[i]['type'])
                            if self.__places[i]['name'] in already_printed:
                                #print("line 395")
                                pass
                            else:
                                print(proposed_index,":", self.__places[i]['name'], self.__places[i]['type'])
                                already_printed.append(self.__places[i]['name'])
                                self.__proposed.append([self.__places[i], proposed_index])
                                proposed_index=proposed_index+1
                        i=i+1
            answer_text="Soll ich dich zu einer der Nummern hinführen?"
            self.speak_text(answer_text)
            print("\n🔊⏎")
            print("Ja bitte?")
            understood =False
            while understood==False:
                self.mySTT.start_mic_listening()
                recognized_text = self.mySTT.get_text_from_recognized_speech()
                if recognized_text == -1:
                    error_msg = "Tut mir Leid, ich konnte das nicht verstehen."
                    self.speak_text(error_msg)
                else:
                    understood=True
                    print("-\""+recognized_text+"\"")
                    if "ja" in recognized_text:
                        if "zu" not in recognized_text:
                            answer_text="Zu dem Ort mit welcher Nummer soll ich dich führen?"
                            self.speak_text(answer_text)
                            print("\n🔊⏎")
                            print("Ja bitte?")
                            understood =False
                            while understood==False:
                                self.mySTT.start_mic_listening()
                                recognized_text = self.mySTT.get_text_from_recognized_speech()
                                if recognized_text == -1:
                                    error_msg = "Tut mir Leid, ich konnte das nicht verstehen."
                                    self.speak_text(error_msg)
                                else:
                                    understood=True
                                    print("-\""+recognized_text+"\"")
                        place_number=0
                        for s in recognized_text.split():
                            try:
                                place_number=w2n.convert(s)
                            except:
                                pass
                            if s.isdigit():
                                place_number=int(s)
                        for place in self.__proposed:
                            if place[1]==int(place_number):
                                #print(place)
                                lat = place[0]['location']['lat']
                                lon = place[0]['location']['lng']
                                self.myDirections.set_current_position(self.myLocation.get_latitude(),self.myLocation.get_longitude())
                                self.myDirections.set_destination_position_lat_lon(lat, lon)
                                travelmode = self.myDirections.translate_travelmode(self.__transportation)
                                text = self.myDirections.say_direction_info(travelmode)
                                self.speak_text(text)
                                self.myDirections.route_to_destination(travelmode)
                                print(lat, lon)                   
        else:
            error_msg = "Tut mir Leid, ich kann dir nicht weiterhelfen."
            self.speak_text(error_msg)
    
    def get_meetings_text(self):
        meetings_text = "Du hast heute "+str(len(self.__meetings))+" Meetings: "
        for e in self.__meetings:
            time_start = e['start'].split("T")[1]
            time_start = time_start.split("+")[0]
            time_end = e['end'].split("T")[1]
            time_end = time_end.split("+")[0]
            text = e['titel']+" an dem Ort "+e['location']+" von "+time_start+" Uhr bis "+time_end+" Uhr. "
            meetings_text = meetings_text + text
        return meetings_text
    
    def get_weather_text(self):
        weather_text = "Es hat momentan "+self.__temperature+". "+self.__weather+" "+self.current_weather['rain?']+". "
        return weather_text
    
    def get_location_text(self):
        location_text = "Du bist gerade in "+self.__town+", "+self.__country+". "
        return location_text
    
    def check_time_for_activities(self, current_time):
        if len(self.__meetings) > 0:
            i = 0
            while self.__meeting_remindered[i] and i<len(self.__meetings)-1:
                i = i + 1
            if not self.__meeting_remindered[i]:
                m = self.__meetings[i]
                meeting_date_time = m['start']
                meeting_date_time = meeting_date_time.split("+")[0]
                meeting_date_time = " ".join(meeting_date_time.split("T"))
                meeting_time = datetime.strptime(meeting_date_time, '%Y-%m-%d %H:%M:%S')
                for minute in [120, 180, 240]:
                    d = current_time + timedelta(minutes=minute)
                    time_remaining = meeting_time - d
                    if -10<=time_remaining.total_seconds()<=0 :
                        self.locker.acquire()
                        time_remaining = meeting_time - current_time
                        if time_remaining.total_seconds() <= 0:
                            pass
                        else:
                            self.propose_free_time_activity(minute)
                        self.locker.release()
    
    def propose_free_time_activity(self, minute):
        if minute>0:
            text = "Du hast noch mindestens "+str(minute/60)+" Stunden bis zum nächsten Meeting. Warum gehst du nich einem deiner Hobbies nach wie "
        else:
            text = "Du hast heute keine Meetings. Warum gehst du nicht einem deiner Hobbies nach wie "
        for hobby in self.__hobby_split:
            if hobby == self.__hobby_split[-1] and len(self.__hobby_split)<1:
                text = text + "oder "+hobby+"."
            elif len(self.__hobby_split)==1:
                text = text + hobby +"."
            else:
                text = text + hobby +","
        text = text + " Alternativ habe ich hier einige Orte an denen du deine Freizeit verbringen könntest."
        self.speak_text(text)
        self.propose_place()
        
    def get_places(self):
        print(". . .")
        result = self.myPlaces.get_nearby_places()
        self.__places=result[0]
        self.__types = result[1]
        self.__types_eng = result[2]                    
    
    def propose_place(self):
        self.get_places()
        
        text = "Ich kann dir "+str(len(self.__places))+" Orte in "
        text = text + " "+ str(len(self.__types))+" Kategorien vorschlagen. Soll ich dir zu einer der Kategorien Details geben?"
        self.speak_text(text)
        pprint.pprint(self.__types)
        
