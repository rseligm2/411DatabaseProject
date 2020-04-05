from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import LoginManager, current_user, login_user, logout_user

from src.app import app, login_manager
from src.form import LoginForm
from src.mongo import users
from src.resources.user import User, load_user


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
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for("index"))
    return render_template("login.html")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/signup", endpoint="signup")
def signup():
    return render_template("signup.html")


@app.route("/contact", endpoint="contact")
def contact():
    return render_template("contact.html")
