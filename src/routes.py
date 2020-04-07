import datetime

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import LoginManager, current_user, login_user, logout_user

from pymongo.errors import WriteError, WriteConcernError
from bson.objectid import ObjectId

from werkzeug.security import generate_password_hash

from src.app import app, login_manager
from src.form import LoginForm, SignupForm
from src.resources.user import User, load_user
from src.mongo import users_col


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/teams/<teams>")
def teams_page(teams):
    pass


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = load_user(form.username.data)
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        print(f"Login Attempt: {login_user(user)}")
        return redirect(url_for("index"))
    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/signup", endpoint="signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = SignupForm()

    if form.validate_on_submit():
        try:
            # Try to create user
            users_col.insert_one(
                {
                    "_id": form.username.data,
                    "username": form.username.data,
                    "password_hash": generate_password_hash(form.password.data),
                    "email": form.email.data,
                    "birthday": datetime.datetime.combine(form.birthday.data, datetime.datetime.min.time()),
                    "comments": [],
                }
            )


            print(load_user(form.username.data))
            print('Created User')
            return redirect(url_for("index"))
        except WriteError:
            flash("Username already taken")
            return redirect(url_for("login"))

    return render_template("signup.html", form=form)


@app.route("/contact", endpoint="contact")
def contact():
    return render_template("contact.html")


@app.route("/profile", endpoint="profile")
def profile():
    return render_template("profile.html")
