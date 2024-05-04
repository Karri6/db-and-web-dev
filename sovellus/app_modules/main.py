from flask import Flask
from dotenv import load_dotenv
from os import getenv, path
from .routes import main as main_blueprint
from .db_instance import db
from flask_login import LoginManager
from app_modules.db_models import User


def create_app():
    """
    Configures the  app after flask is launched, uses flask login to set up
    logging in. Initializes the date and time format used in the html files.

    :return: instance of app
    """
    root_dir = path.abspath(path.join(path.dirname(__file__), '..'))
    db_env_path = path.join(root_dir, "env_files", "db_url.env")
    key_env_path = path.join(root_dir, "env_files", "secret_key.env")

    load_dotenv(db_env_path)
    load_dotenv(key_env_path)

    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = getenv("SECRET_KEY")

    def format_datetime(value, format='%H:%M %d-%m-%Y'):
        """
        Formats a datetime object to a string for the jinja to use
        :param value: the datetime object being formatted
        :param format: string, the format the date is set to
        :return: formatted date time or an empty string if value is none
        """
        if value is None:
            return ""
        return value.strftime(format)

    app.jinja_env.filters['formatdatetime'] = format_datetime

    db.init_app(app)

    manager = LoginManager()
    manager.login_view = "main.login"
    manager.init_app(app)
    
    @manager.user_loader
    def load_user(user_id):
        """
        Uses flask login to fetch a logged-in user
        :param user_id: unique user id
        :return: user object
        """
        return User.query.get(int(user_id))

    app.register_blueprint(main_blueprint)

    return app
