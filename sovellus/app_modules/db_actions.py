"""
Implements the functions for handling db actions

mostly getters and a couple join commands
"""
from .db_models import User, Topic, Thread, Message
from .db_instance import db
from werkzeug.security import check_password_hash
from flask import session


def get_users():
    return User.query.all()


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
