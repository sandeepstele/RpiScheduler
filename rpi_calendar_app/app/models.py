import sqlite3
from datetime import datetime, timedelta
import requests
from flask import Blueprint, render_template

main = Blueprint('main', __name__)

# Establish database connection using relative path
def get_db_connection():
    db_path = 'app/events.db'  # Use relative path
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# Fetch all events
def get_events():
    conn = get_db_connection()
    events = conn.execute('SELECT * FROM events').fetchall()
    conn.close()
    return events

# Add a new event
def add_event(data):
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO events (title, description, start_time, end_time, priority) VALUES (?, ?, ?, ?, ?)',
        (data['title'], data['description'], data['start_time'], data['end_time'], data['priority'])
    )
    conn.commit()
    conn.close()

# Fetch a user by username
def get_user(username):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    return user

# Categorize events by status and date
def categorize_events():
    events = get_events()
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)

    overdue = []
    today_events = []
    tomorrow_events = []
    future_events = []

    for event in events:
        try:
            # Parse ISO 8601 format or fallback to '%Y-%m-%d %H:%M:%S'
            end_date = datetime.strptime(event['end_time'], '%Y-%m-%dT%H:%M').date()
        except ValueError:
            end_date = datetime.strptime(event['end_time'], '%Y-%m-%d %H:%M:%S').date()

        if event['completed'] == 0 and end_date < today:
            overdue.append(event)
        elif end_date == today:
            today_events.append(event)
        elif end_date == tomorrow:
            tomorrow_events.append(event)
        else:
            future_events.append(event)

    return {
        'overdue': sorted(overdue, key=lambda x: x['end_time']),
        'today': sorted(today_events, key=lambda x: x['end_time']),
        'tomorrow': sorted(tomorrow_events, key=lambda x: x['end_time']),
        'future': sorted(future_events, key=lambda x: x['end_time']),
    }

def get_task_statistics():
    conn = get_db_connection()
    completed = conn.execute("SELECT COUNT(*) FROM events WHERE completed = 1").fetchone()[0]
    pending = conn.execute("SELECT COUNT(*) FROM events WHERE completed = 0").fetchone()[0]
    conn.close()
    return {"completed": completed, "pending": pending}

import requests

def get_weather():
    api_key = "213745ddc9d6130ff1335e7b92b93294"  # Replace with your actual API key
    city = "Chennai"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"].capitalize(),
            "icon": f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png"
        }
    return None
