#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 20:09:33 2021
@author: DaVieci
"""

import urllib.request
from bs4 import BeautifulSoup


class SpotifyCharts:
    
    def __init__(self):
        self.__playlist = []
    
    def set_charts_list_by_country(self, country_code):
        spotify_url = "https://spotifycharts.com/regional/"+country_code+"/daily/latest"
        page_data = self.__crawl_webpage_content(spotify_url)
        charts_table = self.__get_charts_table(page_data)
        self.__playlist = self.__parse_table_to_list(charts_table)
    
    def __crawl_webpage_content(self, url):
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        response = opener.open(url)
        html_contents = response.read()
        return html_contents
    
    def __get_charts_table(self, html_contents):
        soup = BeautifulSoup(html_contents, features="lxml")
        table = soup.find("table", attrs={"class":"chart-table"})
        return table
    
    def __parse_table_to_list(self, table):
        datasets = []
        for row in table.find_all("tr")[1:]:
            pos_text = self.__get_position_text(row)
            title_text = self.__get_title_text(row)
            artist_text = self.__get_artist_text(row)
            track_url_text = self.__get_track_url_text(row)
            dataset = [pos_text,title_text,artist_text,track_url_text]
            datasets.append(dataset)
        datasets = datasets[:50] # slice the list at 50 items
        return datasets

    def __get_position_text(self, row):
        pos = row.find("td", attrs={"class":"chart-table-position"})
        pos = pos.get_text()
        pos = pos.strip()
        return pos
    
    def __get_title_text(self, row):
        title = row.find("td", attrs={"class":"chart-table-track"})
        title = title.get_text()
        title = title.split("by ")[0]
        title = title.strip()
        return title
    
    def __get_artist_text(self, row):
        artist = row.find("td", attrs={"class":"chart-table-track"})
        artist = artist.get_text()
        artist = artist.split("by ")[1]
        artist = artist.strip()
        #artist = artist.split(", ") # Do we want to split the artists?
        return artist
    
    def __get_track_url_text(self, row):
        track_url = row.find("td", attrs={"class":"chart-table-image"})
        track_url = track_url.find("a").get('href')
        return track_url
    
    def get_charts_list(self):
        return self.__playlist
