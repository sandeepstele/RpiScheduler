# google_calendar.py
import os
import pickle
import datetime
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def authenticate_google_calendar():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service

def get_google_calendar_events():
    service = authenticate_google_calendar()
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])
    return events

def format_events_for_display():
    events = get_google_calendar_events()
    formatted_events = []

    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        formatted_events.append({
            'title': event['summary'],
            'start_time': start,
            'description': event.get('description', 'No description'),
            'end_time': event['end'].get('dateTime', event['end'].get('date')),
            'priority': 'Urgent' if 'urgent' in event.get('summary', '').lower() else 'Important',
        })
    return formatted_events
