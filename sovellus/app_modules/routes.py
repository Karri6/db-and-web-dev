"""
Handles page requests


"""

from flask import Blueprint, render_template, request, redirect, url_for
from .db_actions import *
from flask_login import logout_user, login_required, login_user, current_user

main = Blueprint("main", __name__)


@main.route("/users")
def show_users():
    users = get_users()
    return render_template("users.html", users=users)


@main.route("/")
@login_required
def index():
    topics = get_topics()
    return render_template("index.html", topics=topics)


@main.route("/topic/<int:topic_id>")
@login_required
def show_topic(topic_id):
    threads = get_threads(topic_id)
    return render_template("topic.html", threads=threads, topic_id=topic_id)


@main.route("/topic/<int:topic_id>/new_thread", methods=["GET", "POST"])
@login_required
def new_thread(topic_id):
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
    return render_template("new_topic.html")


@main.route("/post_topic", methods=["GET","POST"])
@login_required
def post_topic():
    title = request.form.get("title")
    topic_id = add_topic(title, current_user.get_id())
    return redirect(url_for("main.new_thread", topic_id=topic_id))


@main.route("/login", methods=["GET", "POST"])
def login():
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
    logout_user()
    return redirect(url_for("main.login"))


