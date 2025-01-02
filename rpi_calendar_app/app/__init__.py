from flask import Flask
from flask_socketio import SocketIO

socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='your-secret-key'
    )

    from .routes import main
    app.register_blueprint(main)

    socketio.init_app(app)

    return app
