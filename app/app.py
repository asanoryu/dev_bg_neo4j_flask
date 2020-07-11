from flask import Flask, request, session, redirect, render_template, flash, url_for
from app.graph import graph
from app.models import User, get_recent_posts, get_most_followed, recommended_people


app = Flask(__name__)


@app.route("/")
def index():
    username = session.get("username")
    if username:
        posts = get_recent_posts(session["username"])
    else:
        posts = []
    return render_template("index.html", posts=posts)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not User(username).register(password):
            flash("A user already exists.")
        else:
            session["username"] = username
            flash("Logged in.")
            return redirect(url_for("index"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not User(username).verify_password(password):
            flash("Invalid login.")
        else:
            session["username"] = username
            flash("Logged in.")
            return redirect(url_for("index"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("username", None)
    flash("Logged out.")
    return redirect(url_for("index"))


@app.route("/add_post", methods=["POST"])
def add_post():
    text = request.form["text"]
    print(session["username"])
    User(session["username"]).add_post(text)
    flash("Posted.")
    return redirect(url_for("index"))


@app.route("/who_to_follow")
def who_to_follow():
    """Return a list of recomendations based on followed user or a list of most followed people if 
    the user follows no one."""
    if User(session["username"]).get_number_of_followed() == 0:
        who_to_follow = get_most_followed()
    else:
        who_to_follow = recommended_people(session["username"])
    return render_template("who_to_follow.html", who_to_follow=who_to_follow)


@app.route("/follow/<username>")
def follow(username):
    User(session["username"]).follow_user(username)
    flash(f"You are now following {username}")
    return redirect(url_for("index"))
