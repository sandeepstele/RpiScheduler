from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from .models import get_events, add_event, get_user, get_db_connection, categorize_events, get_weather
from .google_calendar import format_events_for_display  # Import the function to fetch Google Calendar events
from functools import wraps
from app.google_calendar import get_google_calendar_events, format_events_for_display

main = Blueprint('main', __name__)

# Decorator to restrict admin-only access
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('role') != 'admin':
            flash("Access denied: Admins only", "danger")
            return redirect(url_for('main.login'))
        return f(*args, **kwargs)
    return decorated_function

# Route to display events for Raspberry Pi (Updated to handle both tasks and Google Calendar events)
@main.route('/display', methods=['GET'])
def display_events():
    sort_by = request.args.get('sort_by', 'date')  # Default sorting by date
    categorized = categorize_events()

    # Fetch weather data for Chennai
    weather = get_weather()

    # Fetch Google Calendar events
    raw_google_events = get_google_calendar_events()  # Fetch events from Google Calendar
    google_events = format_events_for_display(raw_google_events)  # Format the events

    # Add Google Calendar events to the future category
    for event in google_events:
        categorized['future'].append(event)  # Append to the future tasks, for example

    # Sort events by priority if requested
    if sort_by == 'priority':
        for key in ['today', 'tomorrow', 'future']:
            categorized[key] = sorted(
                categorized[key],
                key=lambda x: {'Urgent': 1, 'Important': 2, 'Not Urgent': 3}[x['priority']]
            )

    return render_template(
        'display.html',
        categorized=categorized,
        sort_by=sort_by,
        weather=weather,  # Pass weather data to the template
        google_events=google_events  # Pass Google Calendar events to the template
    )


# Admin dashboard to add/edit events
@main.route('/admin', methods=['GET', 'POST'])
@admin_required
def admin_dashboard():
    if request.method == 'POST':
        data = {
            'title': request.form['title'],
            'description': request.form['description'],
            'start_time': request.form['start_time'],
            'end_time': request.form['end_time'],
            'priority': request.form['priority'],
        }
        add_event(data)
        flash("Event added successfully!", "success")
        return redirect(url_for('main.admin_dashboard'))
    events = get_events()
    return render_template('admin.html', events=events)

# Modify event route
@main.route('/admin/modify/<int:event_id>', methods=['GET', 'POST'])
@admin_required
def modify_event(event_id):
    conn = get_db_connection()
    event = conn.execute('SELECT * FROM events WHERE id = ?', (event_id,)).fetchone()

    if request.method == 'POST':
        # Make sure these form fields are available in the POST request
        new_start_time = request.form.get('start_time')  # Use .get() to avoid KeyError
        new_end_time = request.form.get('end_time')
        new_priority = request.form.get('priority')

        if not new_start_time or not new_end_time or not new_priority:
            flash("Please fill out all the fields.", "danger")
            return redirect(url_for('main.modify_event', event_id=event_id))

        conn.execute(
            'UPDATE events SET start_time = ?, end_time = ?, priority = ? WHERE id = ?',
            (new_start_time, new_end_time, new_priority, event_id)
        )
        conn.commit()
        conn.close()
        flash("Event modified successfully!", "success")
        return redirect(url_for('main.admin_dashboard'))

    conn.close()
    return render_template('modify.html', event=event)

# Mark event as completed
@main.route('/admin/complete/<int:event_id>', methods=['POST'])
@admin_required
def complete_event(event_id):
    conn = get_db_connection()
    conn.execute('UPDATE events SET completed = 1 WHERE id = ?', (event_id,))
    conn.commit()
    conn.close()
    flash("Event marked as completed!", "success")
    return redirect(url_for('main.admin_dashboard'))

# Login route
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Fetch user from the database
        user = get_user(username)
        if user and user['password'] == password:  # Replace with hashed password check in production
            session['role'] = user['role']
            flash("Logged in successfully!", "success")
            return redirect(url_for('main.admin_dashboard'))
        else:
            flash("Invalid username or password", "danger")
            return render_template('login.html')

    # For GET requests, render the login page without any flash messages
    return render_template('login.html')

# Logout route
@main.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully!", "success")
    return redirect(url_for('main.login'))

# Index route
@main.route('/')
def index():
    return redirect(url_for('main.display_events'))

# Delete event route
@main.route('/admin/delete/<int:event_id>', methods=['POST'])
@admin_required
def delete_event(event_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM events WHERE id = ?', (event_id,))
    conn.commit()
    conn.close()
    flash("Event deleted successfully!", "success")
    return redirect(url_for('main.admin_dashboard'))
