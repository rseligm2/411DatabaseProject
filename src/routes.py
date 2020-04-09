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

import requests

import json

@app.route("/")
def index():
    return render_template("index.html")


# @app.route("/teams/<teams>")
# def teams_page(teams):
#     pass


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
                    #"birthday": form.birthday.data,
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


api_header = {}
def api_request(request):

    if request == 'countries':
        url = "https://api-football-v1.p.rapidapi.com/v2/countries"
    else:
        url = f"https://api-football-v1.p.rapidapi.com/v2/teams/search/{request}"

    req = requests.get(url, headers=api_header)
    if not req.content:
        return None

    return json.loads(req.content)


@app.route('/teams', methods=['GET'])
def teams():
    response = api_request('countries')
    return render_template("teams.html", res=response)

# TODO: NOW YOU CANNOT CLICK THE LEFTSIDE BAR AND GET TO THAT COUNTRY_TEAM PAGE. HAVE TO OPEN IT IN A NEW TAB
@app.route('/teams/<country>', methods=['GET'])
def search_team_country(country):

    return render_template('team_country.html', res=api_request('countries'), team_country=api_request(country))


ex_user = {
    "username": "vivian",
    "email": "yuxuanz8@illinois.edu",
    "password_hash": "123456",
    "favorite_player": "Messi",
    "team_flair": "Manchester City",
    "birthday": "1995/10/05",
    "joined_date": "2020/4/1",
    "firstname": "Yuxuan",
    "lastname": "Zhang",
    "country": "United State",
    "city": "Champaign",
    "state": "Illinois",
    "comments": ["hello, comment 1.", 'hello, comment 2.', 'hello, comment 3.', 'hello, comment 4.']
}

# TODO: ADD BACKEND FUNCTION TO FIND USER FROM THE DATABASE. NOW I JUST ADD ONE DICTIONARY TO THE WEBSITE
# TODO: ADD SAVE TO CHANGE THE PROFILE DATA.
@app.route("/<username>/home", endpoint="profile")
def user_home(username):

    return render_template("profile.html", user=ex_user)

# TODO: ACTIVITY TAB: LIST COMMENT, DELETE FUNC

# TODO: ADD SETTING TAB: SUSCRIBE / UNSUSCRIBE

# ============= API ===============
# Allows you to search for a team in relation to a team {name} or {country}
# Spaces must be replaced by underscore for better search performance.
# EX : Real madrid => real_madrid
# =================================
# for now api_request can search for country and team_name.
# !!! may need to change it later for other searches
# =================================

# name should be right and replace space with _
@app.route("/teams/search/<name>")
def team_info(name):

    return render_template("team_info.html", team_info=api_request(name))