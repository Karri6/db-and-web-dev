"""
Handles page requests

imports the flask login to handle permissions and login actions
imports the database handling commands from db actions
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from .db_actions import *
from flask_login import logout_user, login_required, login_user, current_user

main = Blueprint("main", __name__)


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
        log_action(user_id, 'Create Thread', f'User created a new thread in topic ID {topic_id}')

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
        log_action(user_id, 'Post Message', f'User posted a message in thread ID {thread_id}')
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
    log_action(current_user.get_id(), 'Create Topic', f'User created a new topic with ID {topic_id}')
    return redirect(url_for("main.new_thread", topic_id=topic_id))


@main.route("/login", methods=["GET", "POST"])
def login():
    """
    The initial login logic using the flask login library
    :return: render template login html or index/homepage after login
    successful/unsuccessgul
    """
    session.pop('_flashes', None)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = get_user(username)
        if user and check_password_hash(user.password, password):
            login_user(user)
            log_action(user.id, 'login', 'Successful login')
            return redirect(url_for("main.index"))
        else:
            log_action(None, 'login_attempt', 'Failed login attempt for username: {}'.format(username))
            flash("Invalid username or password", "error")
            return render_template("login.html")
    return render_template("login.html")


@main.route("/signup", methods=["GET", "POST"])
def signup():
    """
    initial signup logic, checks if username already exists, if not creates
    a new user and logs them in

    trying out the flash() method usage here

    """
    session.pop('_flashes', None)

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if not username or not password or not confirm_password:
            flash("All fields must be filled.", "error")
            return render_template("signup.html")

        if password != confirm_password:
            flash("The passwords have to match.", "error")
            return render_template("signup.html")

        user_exists = get_user(username)

        if user_exists:
            flash("This Username already exists.", "error")
            return render_template("signup.html")
        else:
            new_user = add_user(username, password)
            login_user(new_user)

            return redirect(url_for("main.index"))

    return render_template("signup.html")


@main.route("/logout")
def logout():
    """
    User logout using the flask login library
    :return:
    """
    logout_user()
    return redirect(url_for("main.login"))


@main.route("/logs")
@login_required
def view_logs():
    """
    Admin page to follow the traffic in the webpage
    :return: renders page to view logs
    """
    user_id = current_user.get_id()

    if get_username(user_id).is_admin() != 'admin':
        abort(403)
    logs = Log.query.order_by(Log.created_at.desc()).all()
    return render_template("logs.html", logs=logs)

@main.errorhandler(403)
def page_forbidden(e):
    """
    Displays the error for forbidden page when a non-Admin user tries to
    access the log-page
    :return:
    """
    return render_template('403.html'), 403


@main.route('/profile')
@login_required
def view_profile():
    """
    Fetches the user profile or creates a new one if one does not exist yet
    :return: renders the user profile page
    """
    user_profile = get_profile(current_user.get_id())
    if not user_profile:
        user_profile = UserProfile(
            user_id=current_user.id,
            first_name='',
            last_name='',
            birthdate=None,
            bio='',
            picture_url='default_image.png'
        )
        db.session.add(user_profile)
        db.session.commit()

        return render_template('profile.html', profile=user_profile, age='not set')

    age = get_age(user_profile.birthdate)

    return render_template('profile.html', profile=user_profile, age=age)


# TODO:
@main.route('/edit_profile', methods=["GET", "POST"])
@login_required
def edit_profile():
    """
    allows user to edit their profile
    :return: html route to the profile editing
    """

    if request.method == "POST":
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        birthdate = request.form.get("birthdate")
        bio = request.form.get("bio")

        user_id = current_user.get_id()

        update_user_info(user_id, firstname, lastname, birthdate, bio)
        user_profile = get_profile(user_id)
        
        age = get_age(user_profile.birthdate)
        return render_template("profile.html", profile=user_profile, age=age)

    return render_template("edit_profile.html")
