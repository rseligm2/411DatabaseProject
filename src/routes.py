import datetime

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import LoginManager, current_user, login_user, logout_user

from pymongo.errors import WriteError, WriteConcernError
from bson.objectid import ObjectId

from werkzeug.security import generate_password_hash

from src.app import app, login_manager
from src.form import LoginForm, SignupForm
from src.resources.user import User, load_user, Comment
from src.mongo import users_col, comments_col, team_comments_col

from src.utils import load_from_database

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
        # print(f"Login Attempt: {}")
        login_user(user)
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
            form_dict = {
                "_id": form.username.data,
                "username": form.username.data,
                "password_hash": generate_password_hash(form.password.data),
                "email": form.email.data,
                # "birthday": form.birthday.data,
                "birthday": form.birthday.data,
            }
            user = User(**form_dict)

            users_col.insert_one(user.to_dict())

            # print(load_user(form.username.data))
            # print("Created User")
            return redirect(url_for("index"))
        except WriteError:
            flash("Username already taken")
            return redirect(url_for("login"))

    return render_template("signup.html", form=form)


@app.route("/contact", endpoint="contact")
def contact():
    return render_template("contact.html")


@app.route("/teams", methods=["GET"])
def teams():
    response = load_from_database("countries")
    return render_template("teams.html", res=response)


# TODO: NOW YOU CANNOT CLICK THE LEFTSIDE BAR AND GET TO THAT COUNTRY_TEAM PAGE. HAVE TO OPEN IT IN A NEW TAB
@app.route("/teams/<country>", methods=["GET"])
def search_team_country(country):

    return render_template(
        "team_country.html",
        res=load_from_database("countries"),
        team_country=load_from_database(country),
    )


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
    "comments": [
        "hello, comment 1.",
        "hello, comment 2.",
        "hello, comment 3.",
        "hello, comment 4.",
    ],
    "favorite_teams": [],
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
    team = load_from_database(name, request_type="teams")

    res = team_comments_col.aggregate(
        [
            {"$match": {"_id": team.name}},
            {"$unwind": "$comments"},
            {
                "$lookup": {
                    "from": "comments",
                    "localField": "comments",
                    "foreignField": "_id",
                    "as": "_id",
                }
            },
            {"$project":{
                "_id": 0,
                "text": "$_id.text",
                "username": "$_id.username"
            }}
        ]
    )
    res = list(res)
    comments = [i["text"][0] if len(i["text"]) > 0 else "" for i in res]
    usernames = [i["username"][0] if len(i["username"]) > 0 else "" for i in res]

    if comments is not None and len(comments) > 0:
        team.comments = [Comment(t, u) for t, u in zip(comments, usernames)]
    return render_template("team_info.html", team_info=team)


@app.route("/teams/search")
def search():
    return render_template("search.html")


@app.route("/submit/comment", methods=["POST"])
def submit_comment():
    if not current_user.is_authenticated:
        flash("User is not logged in")
        return redirect(request.referrer)

    try:
        # Create comment
        resp = comments_col.insert_one({"text": request.form["usercomment"], "username": current_user.get_id()})

        # Insert reference into other
        team_comments_col.update_one(
            {"_id": request.form["team"]},
            {"$setOnInsert": {"comments": []},},
            upsert=True,
        )

        team_comments_col.update_one(
            {"_id": request.form["team"]},
            {"$addToSet": {"comments": resp.inserted_id}},
        )

        users_col.update_one(
            {"_id": current_user.get_id()},
            {"$addToSet": {"comments": resp.inserted_id}},
        )

    except WriteError as e:
        # print(e)
        flash("Failed to post comment")

    # TODO: Create comment
    return redirect(request.referrer)


@app.route("/submit/favorite", methods=["POST"])
def favorite_team():
    if not current_user.is_authenticated:
        return redirect(request.referrer)

    try:
        users_col.update_one(
            {"_id": current_user.get_id()},
            {"$addToSet": {"favorite_teams": request.form["team"]}},
        )
    except ...:
        flash("Failed to favorite team")

    # TODO: Create comment
    return redirect(request.referrer)
