# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 18:31:27 2021

@author: leave
"""

from sqliteAPI import Datenbank
myDB = Datenbank()
keys={}
myDB.insertIntoTableMeetings(keys)

#myDB.createTableKeys()
#myDB.insertIntoTableKeys(keys)
#keys= myDB.getKeys()
print(keys)