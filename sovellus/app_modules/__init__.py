"""
Initializes the package for modularity.


"""

from flask import Flask
from dotenv import load_dotenv
from os import getenv, path
from .routes import main as main_blueprint
from .db_instance import db


directory = path.abspath(path.dirname(__file__))
load_dotenv(path.join(directory, '..', 'db_url.env'))


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    app.register_blueprint(main_blueprint)

    return app
