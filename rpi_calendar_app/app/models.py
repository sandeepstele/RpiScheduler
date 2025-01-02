from flask import Flask
from flask_socketio import SocketIO
from flask_mail import Mail

socketio = SocketIO()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='your-secret-key',
        MAIL_SERVER='smtp.gmail.com',
        MAIL_PORT=587,
        MAIL_USE_TLS=True,
        MAIL_USERNAME='your-email@gmail.com',
        MAIL_PASSWORD='your-email-password'
    )

    from .routes import main
    app.register_blueprint(main)

    socketio.init_app(app)
    mail.init_app(app)

    return app
