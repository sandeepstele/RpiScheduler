from flask import Flask
from flask_socketio import SocketIO

socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='ff47f82c9fc56bb19b61154d4274f882c7b4be9fdd88677fe9583e1cba133161'
    )

    from .routes import main
    app.register_blueprint(main)

    socketio.init_app(app)

    return app
