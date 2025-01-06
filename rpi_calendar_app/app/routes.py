from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from .models import get_events, add_event, get_user_by_username
from functools import wraps

main = Blueprint('main', __name__)

@main.route('/')
def index():
    events = get_events()
    return render_template('index.html', events=events)

@main.route('/event_form')
def event_form():
    return render_template('event_form.html')

@main.route('/events', methods=['POST'])
def create_event():
    data = {
        'title': request.form['title'],
        'description': request.form['description'],
        'start_time': request.form['start_time'],
        'end_time': request.form['end_time'],
    }
    add_event(data)
    return redirect(url_for('main.index'))

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = get_user_by_username(username)
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['role'] = user['role']
            return redirect(url_for('main.index'))

        flash('Invalid username or password')

    return render_template('login.html')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('role') != 'admin':
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@main.route('/admin')
@admin_required
def admin_dashboard():
    return render_template('admin_dashboard.html')
