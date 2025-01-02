from ics import Calendar, Event
from .models import get_db_connection

def export_calendar():
    conn = get_db_connection()
    events = conn.execute('SELECT * FROM events').fetchall()
    conn.close()

    calendar = Calendar()
    for event in events:
        e = Event()
        e.name = event['title']
        e.begin = event['start_time']
        e.end = event['end_time']
        e.description = event['description']
        calendar.events.add(e)

    return str(calendar), 200, {'Content-Type': 'text/calendar'}

def import_calendar(file):
    calendar = Calendar(file.read().decode())
    conn = get_db_connection()

    for event in calendar.events:
        conn.execute(
            'INSERT INTO events (title, description, start_time, end_time) VALUES (?, ?, ?, ?)',
            (event.name, event.description, event.begin, event.end)
        )
    conn.commit()
    conn.close()
