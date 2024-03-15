"""
Handles page requests


"""

from flask import Blueprint, render_template, request, redirect, url_for
from .db_actions import *

main = Blueprint('main', __name__)


@main.route("/users")
def show_users():
    users = get_users()
    return render_template("users.html", users=users)


@main.route("/")
def index():
    topics = get_topics()
    return render_template("index.html", topics=topics)


@main.route("/topic/<int:topic_id>")
def show_topic(topic_id):
    threads = get_threads(topic_id)
    return render_template("topic.html", threads=threads, topic_id=topic_id)


@main.route("/topic/<int:topic_id>/new_thread", methods=["GET", "POST"])
def new_thread(topic_id):
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        user_id = 1
        add_thread(title, content, topic_id, user_id)
        return redirect(url_for('main.show_topic', topic_id=topic_id))
    return render_template("new_thread.html", topic_id=topic_id)


@main.route("/thread/<int:thread_id>", methods=["GET", "POST"])
def show_thread(thread_id):
    if request.method == "POST":
        content = request.form.get("content")
        user_id = 1
        add_message(content, thread_id, user_id)
        return redirect(url_for('main.show_thread', thread_id=thread_id))

    messages = get_messages(thread_id)
    topic_id = get_topic_id(thread_id)
    return render_template("thread.html", messages=messages, thread_id=thread_id, topic_id=topic_id)


