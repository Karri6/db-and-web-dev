"""
Initializes the package for modularity.


"""

from flask import Flask
from dotenv import load_dotenv
from os import getenv, path
from .routes import main as main_blueprint
from .db_instance import db
from flask_login import LoginManager
from app_modules.db_models import User


def create_app():
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
        return User.query.get(int(user_id))

    app.register_blueprint(main_blueprint)

    return app
