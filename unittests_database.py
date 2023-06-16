# -*- coding: utf-8 -*-
"""
Created on Thu Nov 25 11:25:11 2021

@author: leave
"""
 
import unittest
import sqlite3


from Database.sqliteAPI import Datenbank

class test_DB_methods(unittest.TestCase):
    
    def __init__(self, *args, **kwargs):
        super(test_DB_methods, self).__init__(*args, **kwargs)
        self.myDB = Datenbank()
    
    
    def test_get_keys(self):
        keys = self.myDB.getKeys()
        self.assertEqual(len(keys[0]), 3)
        
    def test_create_table_spotify(self):
        self.assertEqual(None, self.myDB.createTableSpotify())
        
    def testInsertTableSpotify_valid_input(self):
        previous_lenth= len(self.myDB.getSpotifyPlaylist())
        playlist = [
            ['1', 'Easy On Me', 'Adele', 'https://open.spotify.com/track/0gplL1WMoJ6iYaPgMCL0gX'],
            ['2', 'titel2', 'artist2', 'https://open.spotify.com/track/0gplL1WMoJ6iYaPgMCL0gX']
            ]
        i=0
        while i<len(playlist):
            self.myDB.insertIntoTableSpotify(playlist[i])
            i=i+1
        self.assertEqual(len(self.myDB.getSpotifyPlaylist()), previous_lenth+2)
        
    def test_insert_table_spotify_insert_nothing(self):
         with self.assertRaises(TypeError):
            self.myDB.insertIntoTableSpotify()
        
    def test_insert_table_spotify_insert_empty(self):
        playlist = []
        with self.assertRaises(IndexError):
            self.myDB.insertIntoTableSpotify(playlist)
        
    def test_get_spotify_playlist(self):
        playlist = [
            ['1', 'Easy On Me', 'Adele', 'https://open.spotify.com/track/0gplL1WMoJ6iYaPgMCL0gX'],
            ['2', 'titel2', 'artist2', 'https://open.spotify.com/track/0gplL1WMoJ6iYaPgMCL0gX']
            ]
        i=0
        while i<len(playlist):
            self.myDB.insertIntoTableSpotify(playlist[i])
            i=i+1
        playlist = self.myDB.getSpotifyPlaylist()
        self.assertEqual(len(playlist[0]), 4)
        
    def test_create_table_meetings(self):
        self.assertEqual(None, self.myDB.createTableMeetings())
        
    def test_insert_table_meetings_valid_input(self):
        previous_lenth= len(self.myDB.getMeetings())
        meetings = {"title":"test",
        "start":"test",
        "end":"test",
        "location":"test"}
        self.myDB.insertIntoTableMeetings(meetings)
        self.assertEqual(len(self.myDB.getSpotifyPlaylist()), previous_lenth+1)
        
    def test_insert_table_meetings_insert_nothing(self):
         with self.assertRaises(TypeError):
            self.myDB.insertIntoTableMeetings()
        
    def test_insert_table_meetings_insert_empty(self):
        meetings = {}
        with self.assertRaises(KeyError):
            self.myDB.insertIntoTableMeetings(meetings)
            
    def test_get_meetings(self):
        meetings = {"title":"test",
        "start":"test",
        "end":"test",
        "location":"test"}
        self.myDB.insertIntoTableMeetings(meetings)
        meetings = self.myDB.getMeetings()
        self.assertEqual(len(meetings[0]), 4)
        
    def test_create_table_preferences(self):
        self.assertEqual(None, self.myDB.createTablePreferences())
        
    def test_insert_table_preferences_valid_input(self):
        preferences = {"name":"test",
        "email":"test",
        "clientID":"test",
        "secretID":"test",
        "hobby":"test",
        "transportation":"test",
        "location":"test",
        "sp_time":"test"}
        self.assertEqual(None, self.myDB.insertIntoTablePreferences(preferences))
        
    def test_insert_table_preferences_insert_nothing(self):
         with self.assertRaises(TypeError):
            self.myDB.insertIntoTablePreferences()
        
    def test_insert_table_preferences_insert_empty(self):
        preferences = {}
        with self.assertRaises(KeyError):
            self.myDB.insertIntoTablePreferences(preferences)
            
    def test_get_preferences(self):
        preferences = self.myDB.getPreferencesForUser("test")
        self.assertEqual(len(preferences[0]), 8)
        
    def test_check_if_user_exists_input_exists(self):
        self.assertTrue(self.myDB.checkIfUserExists("test"))
        
    def test_check_if_user_exists_input_not_existing(self):
        self.assertFalse(self.myDB.checkIfUserExists("SomeTestInputThatDoesn'tExist"))
        
    def test_update_location_valid(self):
        self.assertEqual(None, self.myDB.updateLocation("somewhere else", "test"))
        pref=self.myDB.getPreferencesForUser("test")
        self.assertEqual("somewhere else", pref[0]['location'])
        
#    def test_deleteTestUser(self):
#        con =sqlite3.connect('fridayy.db')
#        
#        cur = con.cursor()
#        cur.execute('''Delete from preferences WHERE name = ?''', ("test",))
#        con.commit()
#        con.close()
#        print("tests deleted")
#        self.assertFalse(self.myDB.checkIfUserExists("test"))
        
    
       
    