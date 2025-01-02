from flask import Blueprint, render_template, request, jsonify
from .models import get_events, add_event, delete_event
from .import_export import export_calendar, import_calendar
from app import socketio

main = Blueprint('main', __name__)

@main.route('/')
def index():
    events = get_events()
    return render_template('index.html', events=events)

@main.route('/events', methods=['POST'])
def create_event():
    data = request.json
    add_event(data)
    socketio.emit('update', data)
    return 'Event created!', 201

@main.route('/export', methods=['GET'])
def export_events():
    return export_calendar()

@main.route('/import', methods=['POST'])
def import_events():
    file = request.files['file']
    import_calendar(file)
    return 'Events imported successfully!'
