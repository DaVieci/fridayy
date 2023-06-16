from __future__ import print_function
import datetime
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

class Calendar:
    def __make_connection(self):
        SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

        if os.path.exists('Calendar/token.json'):
            self.creds = Credentials.from_authorized_user_file('Calendar/token.json', SCOPES)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('Calendar/credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)
            with open('Calendar/token.json', 'w') as token:
                token.write(self.creds.to_json())

    def get_upcomming_events_for_today(self):
        #print(self.creds)
        service = build('calendar', 'v3', credentials=self.creds)

        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' für UTC 
        print('Getting the upcoming 10 events')
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                            maxResults=10, singleEvents=True,
                                            orderBy='startTime').execute()
        events = events_result.get('items', [])

        event_list = []
        
        if not events:
            print('No upcoming events found.')
        date_today = str(datetime.datetime.now()).split(" ")[0]
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            date_event = str(start).split("T")[0]
            if date_event == date_today:
                end = event['end'].get('dateTime', event['end'].get('date'))
                location = ""
                if 'location' in event:
                    location = event['location']
                event_item = {
                    'start': start,
                    'end' : end,
                    'titel' : event['summary'],
                    'location' : location
                }
                event_list.append(event_item)
        #print(event_list)
        return event_list

    def __init__(self):
        self.creds = None
        self.__make_connection()