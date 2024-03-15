"""
Creates a database instance for all modules to use.
Created to remove circular imports that caused the program to crash.
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
