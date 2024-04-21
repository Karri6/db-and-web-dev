"""
Trying the SQLAlchemy's ORM abilities by creating models for the
database tables as classes.


"""
from .db_instance import db
from sqlalchemy.sql import func
from flask_login import UserMixin


class User(UserMixin, db.Model):
    """
    Creates a class for the user object from the users table.
    UserMixin used to use flask login is_active and is_authenticated methods

    > backrefs to topics threads messages and user profile to init one way
    to execute possible delete methods at some point
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(10), nullable=False)
    last_online = db.Column(db.DateTime(timezone=True), default=func.current_timestamp())
    topics = db.relationship('Topic', backref='user', lazy=True, cascade="all, delete-orphan")
    threads = db.relationship('Thread', backref='user', lazy=True, cascade="all, delete-orphan")
    messages = db.relationship('Message', backref='user', lazy=True, cascade="all, delete-orphan")
    profile = db.relationship('UserProfile', backref='user', uselist=False, cascade="all, delete-orphan")

    def is_admin(self):
        return self.role


class Topic(db.Model):
    __tablename__ = 'topics'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.current_timestamp())
    threads = db.relationship('Thread', backref='topic', lazy=True, cascade="all, delete-orphan")


class Thread(db.Model):
    __tablename__ = 'threads'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(1000), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.current_timestamp())
    messages = db.relationship('Message', backref='thread', lazy=True, cascade="all, delete-orphan")


class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1000), nullable=False)
    thread_id = db.Column(db.Integer, db.ForeignKey('threads.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.current_timestamp())


class UserProfile(db.Model):
    __tablename__ = 'user_profiles'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    birthdate = db.Column(db.Date)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    picture_url = db.Column(db.String(255))
    bio = db.Column(db.String(100))


class Log(db.Model):
    __tablename__ = 'log'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    action = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), default=func.current_timestamp())
