"""
Handles page requests

imports the flask login to handle permissions and login actions
imports the database handling commands from db actions
"""

from flask import Blueprint, render_template, request, redirect, url_for
from .db_actions import *
from flask_login import logout_user, login_required, login_user, current_user

main = Blueprint("main", __name__)


# to be deleted, from first database tests,
# alternatively, might repurpose for admin use
@main.route("/users")
def show_users():
    users = get_users()
    return render_template("users.html", users=users)


@main.route("/")
@login_required
def index():
    """
    Index / homepage of the app, initial view of the topics in the app.
    :return: render template index.html
    """
    topics = get_topics()
    return render_template("index.html", topics=topics)


@main.route("/topic/<int:topic_id>")
@login_required
def show_topic(topic_id):
    """
    Moves user to view the thread list under a chosen topic
    :param topic_id: unique id for the topic
    :return: render template of topic.html
    """
    threads = get_threads(topic_id)
    topic = get_topic(topic_id)
    return render_template("topic.html", topic=topic, threads=threads)


@main.route("/topic/<int:topic_id>/new_thread", methods=["GET", "POST"])
@login_required
def new_thread(topic_id):
    """
    Enables creating new threads under a given topic
    :param topic_id: unique topic id where user is creating the thread
    :return: render template of the new thread
    """
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        user_id = current_user.get_id()
        add_thread(title, content, topic_id, user_id)
        return redirect(url_for("main.show_topic", topic_id=topic_id))
    return render_template("new_thread.html", topic_id=topic_id)


@main.route("/thread/<int:thread_id>", methods=["GET", "POST"])
@login_required
def show_thread(thread_id):
    """
    Used to view a chosen thread under a topic
    :param thread_id: unique thread id of the chosen thread
    :return: render template of the thread html
    """
    if request.method == "POST":
        content = request.form.get("content")
        user_id = current_user.get_id()
        add_message(content, thread_id, user_id)
        return redirect(url_for("main.show_thread", thread_id=thread_id))

    messages = get_message_user_join(thread_id)
    thread = get_thread_user_join(thread_id)
    topic_id = get_topic_id(thread_id)
    return render_template("thread.html", messages=messages, thread=thread,
                           thread_id=thread_id, topic_id=topic_id)


@main.route("/new_topic", methods=["GET", "POST"])
@login_required
def new_topic():
    """
    Enables posting a new topic on the homepage
    :return: render template of new topic
    """
    return render_template("new_topic.html")


@main.route("/post_topic", methods=["GET", "POST"])
@login_required
def post_topic():
    """
    Moves user to create a new thread under the topic they have just created.
    :return: redirect to new thread
    """
    title = request.form.get("title")
    topic_id = add_topic(title, current_user.get_id())
    return redirect(url_for("main.new_thread", topic_id=topic_id))


@main.route("/login", methods=["GET", "POST"])
def login():
    """
    The initial login logic using the flask login library
    :return: render template login html or index/homepage after login
    successful/unsuccessgul
    """
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("main.index"))
        else:
            return render_template("login.html", error="Invalid username or password")
    return render_template("login.html")


@main.route("/logout")
def logout():
    """
    User logout using the flask login library
    :return:
    """
    logout_user()
    return redirect(url_for("main.login"))


