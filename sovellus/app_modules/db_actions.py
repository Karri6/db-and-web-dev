"""
Implements the functions for handling db actions


"""
from .db_models import User, Topic, Thread, Message
from .db_instance import db


def get_users():
    return User.query.all()


def get_topics():
    return Topic.query.all()


def get_threads(topic_id):
    return Thread.query.filter_by(topic_id=topic_id).all()


def get_messages(thread_id):
    return Message.query.filter_by(thread_id=thread_id).all()


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