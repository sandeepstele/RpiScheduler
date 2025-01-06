import sqlite3

def get_db_connection():
    conn = sqlite3.connect('app/events.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_events():
    conn = get_db_connection()
    events = conn.execute('SELECT * FROM events').fetchall()
    conn.close()
    return events

def add_event(data):
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO events (title, description, start_time, end_time) VALUES (?, ?, ?, ?)',
        (data['title'], data['description'], data['start_time'], data['end_time'])
    )
    conn.commit()
    conn.close()

def get_user_by_username(username):
    conn = get_db_connection()
    user = conn.execute(
        'SELECT * FROM users WHERE username = ?', (username,)
    ).fetchone()
    conn.close()
    return user
