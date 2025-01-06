import sqlite3
from datetime import datetime, timedelta

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
