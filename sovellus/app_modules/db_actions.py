"""
Implements sql queries to fetch data from the database.

Changed to regular text based sql queries, but combined with the previous
logic that used the class based instance creation.
"""
import datetime
from .db_models import *
from .db_instance import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask import session
from sqlalchemy import text


def get_user(username):
    """
    Fetches user by username and creates an instance of them.
    :param username: unique username
    :return: user object if user was found
    """
    sql = text("SELECT id, username, password, role, last_online FROM users WHERE username = :username")
    result = db.session.execute(sql, {'username': username})
    user_data = result.fetchone()
    if user_data:
        user = User(
            id=user_data[0],
            username=user_data[1],
            password=user_data[2],
            role=user_data[3],
            last_online=user_data[4]
        )
        return user
    return None


def get_topic(topic_id):
    """
    Fetches a topic by topic id and creates an instance of it.
    :param topic_id: unique id
    :return: topic object if topic was found
    """
    sql = text("SELECT id, title, user_id, created_at FROM topics WHERE id = :topic_id")
    result = db.session.execute(sql, {'topic_id': topic_id})
    topic_data = result.fetchone()
    if topic_data:
        topic = Topic(
            id=topic_data[0],
            title=topic_data[1],
            user_id=topic_data[2],
            created_at=topic_data[3]
        )
        return topic
    return None


def get_thread(thread_id):
    """
    Fetches a thread by thread id and creates an instance of it.
    :param thread_id: unique id
    :return: topic object if thread was found
    """
    sql = text("SELECT id, title, content, topic_id, user_id, created_at FROM threads WHERE id = :thread_id")
    result = db.session.execute(sql, {'thread_id': thread_id})
    thread_data = result.fetchone()
    if thread_data:
        thread = Thread(
            id=thread_data[0],
            title=thread_data[1],
            content=thread_data[2],
            topic_id=thread_data[3],
            user_id=thread_data[4],
            created_at=thread_data[5]
        )
        return thread
    return None


def get_topics():
    """
    Fetches all topics in the database and creates instances of them.
    :return: list of all topics as instances
    """
    sql = text("SELECT id, title, user_id, created_at FROM topics")
    result = db.session.execute(sql)
    return [Topic(id=row[0], title=row[1], user_id=row[2], created_at=row[3]) for row in result.fetchall()]


def get_threads(topic_id):
    """
    Fetches all threads in the database and creates instances of them.
    :return: list of all threads as instances
    """
    sql = text("SELECT id, title, content, topic_id, user_id, created_at FROM threads WHERE topic_id = :topic_id")
    result = db.session.execute(sql, {'topic_id': topic_id})
    return [Thread(id=row[0], title=row[1], content=row[2], topic_id=row[3], user_id=row[4], created_at=row[5]) for row in result.fetchall()]


def get_messages(thread_id):
    """
    Fetches all messages in the database and creates instances of them.
    :return: list of all messages as instances
    """

    sql = text("SELECT id, content, thread_id, user_id, created_at FROM messages WHERE thread_id = :thread_id")
    result = db.session.execute(sql, {'thread_id': thread_id})
    return [Message(id=row[0], content=row[1], thread_id=row[2], user_id=row[3], created_at=row[4]) for row in result.fetchall()]


def get_profile(user_id):
    """
    Fetches user profile from the database
    :param user_id: unique user id
    :return: instance of the user profile
    """
    sql = text("SELECT user_id, birthdate, first_name, last_name, picture_url, bio FROM user_profiles WHERE user_id = :user_id")
    result = db.session.execute(sql, {'user_id': user_id})
    profile_data = result.fetchone()
    if profile_data:
        profile = UserProfile(
            user_id=profile_data[0],
            birthdate=profile_data[1],
            first_name=profile_data[2],
            last_name=profile_data[3],
            picture_url=profile_data[4],
            bio=profile_data[5]
        )
        return profile
    return None


def get_message_user_join(thread_id):
    """
    Creates a joined list of the messages and users to enable
    displaying user info with the messages.
    :param thread_id: unique thread id
    :return: list of all joined instances
    """
    sql = text(""" SELECT m.content, u.username, m.created_at FROM messages m
        JOIN users u ON u.id = m.user_id WHERE m.thread_id = :thread_id """)
    result = db.session.execute(sql, {'thread_id': thread_id})
    return [
        {
            'content': row[0],
            'username': row[1],
            'created_at': row[2]
        } for row in result.fetchall()
    ]


def get_thread_user_join(thread_id):
    """
    Creates a joined list of the threads and users to enable
    displaying user info with the threads.
    :param thread_id: unique thread id
    :return: list of all joined instances
    """
    sql = text("""SELECT t.id, t.title, t.content, u.username, t.created_at FROM threads t
        JOIN users u ON u.id = t.user_id WHERE t.id = :thread_id""")
    result = db.session.execute(sql, {'thread_id': thread_id})
    thread_data = result.fetchone()
    if thread_data:
        return {
            'id': thread_data[0],
            'title': thread_data[1],
            'content': thread_data[2],
            'username': thread_data[3],
            'created_at': thread_data[4]
        }
    return None


def add_thread(title, content, topic_id, user_id):
    """
    Adds new thread to the database
    :param title: thread title
    :param content: thread content
    :param topic_id: unique topic id of the topic where the thread is
    :param user_id: unique user id of the thread creator
    :return:
    """
    sql = text("""INSERT INTO threads (title, content, topic_id, user_id, created_at)
        VALUES (:title, :content, :topic_id, :user_id, CURRENT_TIMESTAMP)
        RETURNING id""")
    result = db.session.execute(sql, {'title': title, 'content': content, 'topic_id': topic_id, 'user_id': user_id})
    db.session.commit()
    return result.fetchone()[0]


def add_message(content, thread_id, user_id):
    """
    Adds a new message to the database
    :param content: message content
    :param thread_id: unique id of the messages thread
    :param user_id: unique id of the user who posted the message
    :return: the new message
    """
    sql = text("""INSERT INTO messages (content, thread_id, user_id, created_at)
        VALUES (:content, :thread_id, :user_id, CURRENT_TIMESTAMP) RETURNING id""")
    result = db.session.execute(sql, {'content': content, 'thread_id': thread_id, 'user_id': user_id})
    db.session.commit()
    return result.fetchone()[0]


def add_topic(title, user_id):
    """
    Adds a new topic to the database
    :param title: title for the topic
    :param user_id: unique id of the user who created the topic
    :return: the new topic
    """
    sql = text("""INSERT INTO topics (title, user_id, created_at)
        VALUES (:title, :user_id, CURRENT_TIMESTAMP) RETURNING id""")
    result = db.session.execute(sql, {'title': title, 'user_id': user_id})
    db.session.commit()
    return result.fetchone()[0]


def add_user(username, password):
    """
    Creates a new user to the database
    :param username: unique username of the user
    :param password: unhashed password of the user
    :return: instance of the new user
    """
    hashed_password = generate_password_hash(password)
    sql = text("""INSERT INTO users (username, password, role, last_online)
        VALUES (:username, :hashed_password, 'user', CURRENT_TIMESTAMP) RETURNING id""")
    db.session.execute(sql, {'username': username, 'hashed_password': hashed_password})
    db.session.commit()
    return get_user(username)


def login_user(username, password):
    """
    Logins a user
    :param username: unique username
    :param password: users password hashed
    :return: bool, was the login successful
    """
    user = get_user(username)
    if user and check_password_hash(user.password, password):
        session["user_id"] = user.id
        return True
    return False


def log_action(user_id, action, description):
    """
    Adds a new log event to the admin logs in the database
    :param user_id: unique id of the user whose event is stored
    :param action: event being logged
    :param description: short detail of what happened
    """
    sql = text("""INSERT INTO log (user_id, action, description, created_at)
        VALUES (:user_id, :action, :description, CURRENT_TIMESTAMP) RETURNING id""")
    db.session.execute(sql, {'user_id': user_id, 'action': action, 'description': description})
    db.session.commit()


def get_userrole(user_id):
    """
    Enables checking if a user is admin or not
    :param user_id: unique user id
    :return: user role
    """
    sql = text("SELECT role FROM users WHERE id = :user_id")
    result = db.session.execute(sql, {'user_id': user_id})
    user_data = result.fetchone()
    return user_data[0] if user_data else None


def get_topic_id(thread_id):
    """
    Fetches topic id to help page navigation.
    :param thread_id: unique id of the thread
    :return: topic id
    """
    sql = text("SELECT topic_id FROM threads WHERE id = :thread_id")
    result = db.session.execute(sql, {'thread_id': thread_id})
    fetched = result.fetchone()
    return fetched[0] if fetched else None


def update_user_info(user_id, firstname, lastname, birthdate, bio):
    """
    Updates user profile information in the database
    :param user_id: unique user id
    :param firstname: users name
    :param lastname: users lastname
    :param birthdate: users birthdate
    :param bio: users bio
    """
    updates = []
    params = {'user_id': user_id}

    if firstname:
        updates.append("first_name = :firstname")
        params['firstname'] = firstname

    if lastname:
        updates.append("last_name = :lastname")
        params['lastname'] = lastname

    if birthdate:
        formatted_date = format_date(birthdate)
        updates.append("birthdate = :birthdate")
        params['birthdate'] = formatted_date

    if bio:
        updates.append("bio = :bio")
        params['bio'] = bio

    if updates:
        update_sql = "UPDATE user_profiles SET " + ", ".join(updates) + " WHERE user_id = :user_id"
        db.session.execute(text(update_sql), params)
        db.session.commit()


def format_date(birthdate):
    """
    Formats date object to proper format
    :param birthdate: users birthdate
    :return: parsed date
    """
    parsed_date = datetime.datetime.strptime(birthdate, '%Y-%m-%d').date()
    return parsed_date.strftime('%d/%m/%Y')


def get_age(birthdate):
    """
    Calculates users age
    :param birthdate: users birthdate
    :return: Age or 'Not Set' if no date stored
    """
    if birthdate is None:
        return 'Not set'

    today = datetime.datetime.now()
    return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
