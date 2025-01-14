import os
import datetime

DEBUG_MODE = True  # Set this flag to True to skip Google Auth during debugging

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
TOKEN_FILE = os.path.join(os.path.dirname(__file__), '../token.json')
CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), '../credentials.json')

def get_google_calendar_events(max_results=10):
    if DEBUG_MODE:
        print("[DEBUG] Skipping Google Calendar API initialization")
        # Return mock data for debugging
        return [
            {
                'summary': 'Sample Event 1',
                'start_time': '2025-01-01T10:00:00',
                'description': 'This is a mock event for debugging',
                'location': 'Online',
            },
            {
                'summary': 'Sample Event 2',
                'start_time': '2025-01-02T14:00:00',
                'description': 'Another mock event',
                'location': 'Office',
            },
        ]

    # If not in DEBUG_MODE, initialize Google Auth
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build

    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(
        calendarId='primary', timeMin=now,
        maxResults=max_results, singleEvents=True,
        orderBy='startTime').execute()
    events = events_result.get('items', [])
    if not events:
        print('No upcoming events found.')
        return []
    return format_events_for_display(events)

def format_events_for_display(events):
    formatted_events = []
    for event in events:
        start = event.get('start', {}).get('dateTime') or event.get('start', {}).get('date')
        formatted_events.append({
            'summary': event.get('summary', 'No Title'),
            'start_time': start,
            'description': event.get('description', 'No description'),
            'location': event.get('location', 'No location'),
        })
    return formatted_events
