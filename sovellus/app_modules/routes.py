"""
Handles page requests, uses db_actions to make sql queries.

imports the flask login to handle permissions and login actions
imports the database handling commands from db actions
"""
import secrets
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
    Handles posting a new thread under a topic
    :param topic_id: unique id of the topic
    :return: render html of the topic with the new thread posted under it
    """
    if request.method == "POST":
        csrf_token = session.get('csrf_token')
        form_csrf_token = request.form.get('csrf_token')

        if not csrf_token or form_csrf_token != csrf_token:
            abort(403)

        title = request.form.get("title")
        content = request.form.get("content")
        user_id = current_user.get_id()
        add_thread(title, content, topic_id, user_id)
        log_action(user_id, 'Create Thread', f'User created a new thread in topic ID {topic_id}')

        session['csrf_token'] = secrets.token_hex(16)
        return redirect(url_for("main.show_topic", topic_id=topic_id))

    session['csrf_token'] = secrets.token_hex(16)
    return render_template("new_thread.html", topic_id=topic_id, csrf_token=session['csrf_token'])


@main.route("/thread/<int:thread_id>", methods=["GET", "POST"])
@login_required
def show_thread(thread_id):
    """
    Handles showing a thread, as well as posting new messages into it
    :param thread_id: unique thread id
    :return: render html of the thread
    """
    if request.method == "POST":
        form_csrf_token = request.form.get("csrf_token")
        if form_csrf_token != session.get("csrf_token"):
            abort(403)

        content = request.form.get("content")
        user_id = current_user.get_id()
        add_message(content, thread_id, user_id)
        log_action(user_id, 'Post Message', f'User posted a message in thread ID {thread_id}')

        session["csrf_token"] = secrets.token_hex(16)

        return redirect(url_for("main.show_thread", thread_id=thread_id))

    session["csrf_token"] = secrets.token_hex(16)
    messages = get_message_user_join(thread_id)
    thread = get_thread_user_join(thread_id)
    topic_id = get_topic_id(thread_id)
    return render_template("thread.html", messages=messages, thread=thread,
                           thread_id=thread_id, topic_id=topic_id, csrf_token=session["csrf_token"])


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
    Enables posting a new topic on the homepage
    :return: render template of new topic
    """
    if request.method == "POST":
        form_csrf_token = request.form.get("csrf_token")
        if form_csrf_token != session.get("csrf_token"):
            abort(403)

        title = request.form.get("title")
        topic_id = add_topic(title, current_user.get_id())
        log_action(current_user.get_id(), 'Create Topic', f'User created a new topic with ID {topic_id}')

        session["csrf_token"] = secrets.token_hex(16)

        return redirect(url_for("main.new_thread", topic_id=topic_id))

    session["csrf_token"] = secrets.token_hex(16)
    return render_template("new_topic.html", csrf_token=session["csrf_token"])


@main.route("/login", methods=["GET", "POST"])
def login():
    """
    Handles user login using flask login library
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
            session["csrf_token"] = secrets.token_hex(16)
            return redirect(url_for("main.index"))
        else:
            log_action(None, 'login_attempt', 'Failed login attempt for username: {}'.format(username))
            flash("Invalid username or password", "error")
            return render_template("login.html")

    return render_template("login.html")


@main.route("/signup", methods=["GET", "POST"])
def signup():
    """
    Handles user sign up using flask login library
    :return: render template signup html or index/homepage after login
    successful/unsuccessgul
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
            session["csrf_token"] = secrets.token_hex(16)
            return redirect(url_for("main.index"))

    return render_template("signup.html")


@main.route("/logout")
def logout():
    """
    User logout using the flask login library
    :return: renders login html
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

    if get_userrole(user_id) != 'admin':
        abort(401)
    logs = Log.query.order_by(Log.created_at.desc()).all()
    return render_template("logs.html", logs=logs)


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


@main.route('/edit_profile', methods=["GET", "POST"])
@login_required
def edit_profile():
    """
    Allows user to edit their profile
    :return: render user profile html
    """
    if request.method == "POST":
        form_csrf_token = request.form.get("csrf_token")
        if form_csrf_token != session.get("csrf_token"):
            abort(403)

        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        birthdate = request.form.get("birthdate")
        bio = request.form.get("bio")

        user_id = current_user.get_id()
        update_user_info(user_id, firstname, lastname, birthdate, bio)
        user_profile = get_profile(user_id)
        age = get_age(user_profile.birthdate)

        session["csrf_token"] = secrets.token_hex(16)
        return render_template("profile.html", profile=user_profile, age=age)

    session["csrf_token"] = secrets.token_hex(16)
    return render_template("edit_profile.html", csrf_token=session["csrf_token"])


@main.app_errorhandler(500)
def internal_server_error(e):
    """
    Displays error for any internal server error
    :return: renders 500.html error page
    """
    user_id = current_user.get_id()
    log_action(user_id, 'Error', f'User faced an internal error {e}')
    return render_template('500.html'), 500


@main.errorhandler(401)
def unauthorized_error(e):
    """
    Displays the error for forbidden page when a non-Admin user tries to
    access the log-page
    :return:
    """
    user_id = current_user.get_id()
    log_action(user_id, 'Error', f'User faced an unauthorized error: {e}')
    return render_template('401.html'), 401


@main.app_errorhandler(403)
def forbidden_action(e):
    """
    Displays error for forbidden page when a user tries to submit a form
    without a csrf token
    :return:
    """
    user_id = current_user.get_id()
    log_action(user_id, 'Error', f'User faced a forbidden action error: {e}')
    return render_template('403.html'), 403
