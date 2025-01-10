# app/google_calendar.py
import os
import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def get_google_calendar_events():
    creds = None
    # The file token.json stores the user's access and refresh tokens
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If no credentials, let user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Build the calendar API service
    service = build('calendar', 'v3', credentials=creds)

    # Get upcoming events
    events_result = service.events().list(
        calendarId='primary', timeMin=datetime.datetime.utcnow().isoformat() + 'Z',
        maxResults=10, singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
        return []
    
    formatted_events = format_events_for_display(events)
    return formatted_events

def format_events_for_display(events):
    formatted_events = []
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        formatted_events.append({
            'summary': event['summary'],
            'start_time': start,
            'description': event.get('description', 'No description'),
            'location': event.get('location', 'No location'),
        })
    return formatted_events
