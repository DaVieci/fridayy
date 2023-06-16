# -*- coding: utf-8 -*-
"""
Created on Thu Oct 21 11:37:46 2021

@author: leave
"""
import sqlite3
#PRAGMA encoding='UTF-16BE'

class Datenbank:
    def __init__(self):
        self.createTableSpotify()
        self.createTablePreferences()
        self.createTableMeetings()
        
    def createTableKeys(self):
        con =sqlite3.connect('fridayy.db')
        
        cur = con.cursor()
        # Create table
        cur.execute('''Drop table if exists keys''')
        cur.execute('''CREATE TABLE IF NOT EXISTS keys
                   (weather_key varchar(100), places_key varchar(100), directions_key varchar(100))''')
        con.commit()
        con.close()
        
    def insertIntoTableKeys(self, row):
        
        con =sqlite3.connect('fridayy.db')
        
        cur = con.cursor()
        # Insert into table
        cur.execute('''INSERT INTO keys VALUES (?,?,?)''', 
                    (row[0], row[1], row[2]))
        con.commit()
        con.close()
        
    def getKeys(self):
        
        con =sqlite3.connect('fridayy.db')
        
        cur = con.cursor()
        # Create table
        cur.execute('''Select * from keys''')
        con.commit()
        result = cur.fetchall()
        #print(result[0][0])
        keys = []
        for row in result:
            keys.append({"weather_key":row[0],
        "places_key":row[1],
        "directions_key":row[2]})
        con.close()
    
        return(keys)

    def createTableSpotify(self):
        con =sqlite3.connect('fridayy.db')
        
        cur = con.cursor()
        # Create table
        cur.execute('''Drop table if exists spotify''')
        cur.execute('''CREATE TABLE spotify
                   (position varchar(5), title varchar(100), artist varchar(100),
                    trackURL varchar(255))''')
        con.commit()
        con.close()
        
    def insertIntoTableSpotify(self, row):
        
        con =sqlite3.connect('fridayy.db')
        
        cur = con.cursor()
        # Insert into table
        cur.execute('''INSERT INTO spotify VALUES (?,?,?,?)''', 
                    (row[0], row[1], row[2],row[3]))
        con.commit()
        con.close()
        
    def getSpotifyPlaylist(self):
        
        con =sqlite3.connect('fridayy.db')
        
        cur = con.cursor()
        # Create table
        cur.execute('''Select * from spotify''')
        con.commit()
        result = cur.fetchall()
        #print(result[0][0])
        playlist = []
        for row in result:
            playlist.append({"position":row[0],
        "title":row[1],
        "artist":row[2],
        "trackURL":row[3]})
        con.close()
    
        return(playlist)     
    
        
    def createTableMeetings(self):
        
        con =sqlite3.connect('fridayy.db')
        
        cur = con.cursor()
        # Create table
        cur.execute('''Drop table if exists meetings''')
        cur.execute('''CREATE TABLE meetings
                   (title varchar(100), start varchar(100),
                    end varchar(100), location varchar(100))''')
        con.commit()
        con.close()
    
    def insertIntoTableMeetings(self, row):
       
        con =sqlite3.connect('fridayy.db')
        
        cur = con.cursor()
        cur.execute('''INSERT INTO meetings VALUES (?,?,?,?)''', 
                    (row["title"], row["start"], row["end"],row["location"]))
        con.commit()
        con.close()  
        
    def getMeetings(self):
        
        con =sqlite3.connect('fridayy.db')
        
        cur = con.cursor()
        # Create table
        cur.execute('''Select * from meetings''')
        con.commit()
        result = cur.fetchall()
        #print(result[0][0])
        meetings = []
        for row in result:
            meetings.append({"title":row[0],
        "start":row[1],
        "end":row[2],
        "location":row[3]})
        con.close()
    
        return(meetings)  
        
    def createTablePreferences(self):
        
        con =sqlite3.connect('fridayy.db')
        
        cur = con.cursor()
        #cur.execute('''Drop table if exists preferences''')
        #print("dropped")
        cur.execute('''CREATE TABLE IF NOT EXISTS preferences
                   (name varchar(50), email varchar(255), clientID varchar(100),
                    secretID varchar(255), hobby varchar(100), transportation varchar(100),
                    location varchar(100), sp_time varchar(100))''')
        con.commit()
        con.close()
    
    def getPreferencesForUser(self, user_name):
        
        con =sqlite3.connect('fridayy.db')
        
        cur = con.cursor()
        # Create table
        cur.execute('''Select * from preferences where name = ?''', (user_name,))
        con.commit()
        result = cur.fetchall()
        #print(result[0][0])
        rowarray_list = []
        for row in result:
            rowarray_list.append({"name":row[0],
        "email":row[1],
        "clientID":row[2],
        "secretID":row[3],
        "hobby":row[4],
        "transportation":row[5],
        "location":row[6],
        "sp_time":row[7]})
        #print(rowarray_list[1]['name'])
        con.close()
        return(rowarray_list)    
        
    def checkIfUserExists(self, inputName):
        
        con =sqlite3.connect('fridayy.db')
        
        cur = con.cursor()
        # Create table
        cur.execute('''Select name from preferences''')
        result = cur.fetchall()
        res_list = []
        for row in result:
            res_list.append({"name":row[0]})
        #print(res_list)
        #print(len(res_list))
       
        exists=False
        i=0
        while i < len(res_list):
            if res_list[i]['name']==inputName:
               exists= True
               break
            i=i+1
        con.commit()
        con.close()  
        return exists
        
    def insertIntoTablePreferences(self, row):
        
        con =sqlite3.connect('fridayy.db')
        
        cur = con.cursor()
        # Create table
        cur.execute('''INSERT INTO preferences VALUES (?,?,?,?,?,?,?,?)''', 
                    (row["name"], row["email"], row["clientID"],row["secretID"], 
                    row["hobby"], row["transportation"],row["location"], row["sp_time"]))
        con.commit()
        con.close()
        
    
    
    def updateLocation(self, new_location, user_name):
        
        con =sqlite3.connect('fridayy.db')
        
        cur = con.cursor()
        cur.execute('''UPDATE preferences SET location = ? WHERE name = ?''', (new_location, user_name))
        con.commit()
        con.close()
        #print("table updated")
    
    preferences={
        "name":"test2",
        "email":"test",
        "clientID":"test",
        "secretID":"test",
        "hobby":"test",
        "transportation":"test",
        "location": "here"
        }
#test= sqliteAPICheckIfUserExists("test2")
#test= sqliteAPIGetPreferencesForUser("test2")
#print(test)
#playlist = [
 # ['1', 'Easy On Me', 'Adele', 'https://open.spotify.com/track/0gplL1WMoJ6iYaPgMCL0gX'],
 # ['2', 'titel2', 'artist2', 'https://open.spotify.com/track/0gplL1WMoJ6iYaPgMCL0gX']
#]
#print(playlist[0][1])
#i=0
#sqliteAPICreateTableSpotify()
#while i<len(playlist):
  #  print(playlist[i])
    #sqliteAPIInsertIntoTableSpotify(playlist[i])
   # i=i+1
#sqliteAPICreateTableMeetings()    
#events=sqliteAPIGetMeetings()
#print(events)

