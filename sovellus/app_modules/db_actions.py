"""
Implements the functions for handling db actions

mostly getters and a couple join commands
"""
import datetime

from .db_models import *
from .db_instance import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask import session


def get_users():
    return User.query.all()


def get_user(username):
    return User.query.filter_by(username=username).first()


def get_topic(topic_id):
    return Topic.query.get_or_404(topic_id)


def get_topics():
    return Topic.query.all()


def get_threads(topic_id):
    return Thread.query.filter_by(topic_id=topic_id).all()


def get_messages(thread_id):
    return Message.query.filter_by(thread_id=thread_id).all()


def get_thread(thread_id):
    return Thread.query.filter_by(id=thread_id).first()


def add_thread(title, content, topic_id, user_id):
    new_thread = Thread(title=title, content=content, topic_id=topic_id, user_id=user_id)
    db.session.add(new_thread)
    db.session.commit()


def add_message(content, thread_id, user_id):
    new_message = Message(content=content, thread_id=thread_id, user_id=user_id)
    db.session.add(new_message)
    db.session.commit()


def get_topic_id(thread_id):
    thread = Thread.query.filter_by(id=thread_id).first()
    return thread.topic_id


def add_topic(title, user_id):
    new_topic = Topic(title=title, user_id=user_id)
    db.session.add(new_topic)
    db.session.commit()
    return new_topic.id


def login_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        session["user_id"] = user.id
        return True
    return False


def get_message_user_join(thread_id):
    messages = db.session.query(
        Message.content,
        User.username.label("username"),
        Message.created_at).join(
        User, User.id == Message.user_id).filter(
        Message.thread_id == thread_id).all()
    return messages


def get_thread_user_join(thread_id):
    thread = db.session.query(
        Thread.id,
        Thread.title,
        Thread.content,
        User.username.label("username"),
        Thread.created_at).join(
        User, User.id == Thread.user_id).filter(
        Thread.id == thread_id).first()
    return thread


def get_username(user_id):
    return User.query.filter_by(id=user_id).first()


def add_user(username, password):
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password, role="user")
    db.session.add(new_user)
    db.session.commit()
    return new_user


def log_action(user_id, action, description):
    log_entry = Log(user_id=user_id, action=action, description=description)
    db.session.add(log_entry)
    db.session.commit()


def get_profile(user_id):
    return UserProfile.query.filter_by(user_id=user_id).first()


def update_user_info(user_id, firstname, lastname, birthdate, bio):
    user_profile = UserProfile.query.filter_by(user_id=user_id).first()

    if firstname:
        user_profile.first_name = firstname

    if lastname:
        user_profile.last_name = lastname

    if birthdate:

        formatted_date = format_date(birthdate)
        user_profile.birthdate = formatted_date

    if bio:
        user_profile.bio = bio

    db.session.commit()


def format_date(birthdate):
    parsed_date = datetime.datetime.strptime(birthdate, '%Y-%m-%d').date()
    return parsed_date.strftime('%d/%m/%Y')


def get_age(birthdate):
    today = datetime.datetime.now()
    return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
