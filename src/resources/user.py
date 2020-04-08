from dataclasses import *
from typing import *

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.urls import url_parse

from src.app import app, login_manager
from src.mongo import users

login_manager.login_view = "login"


@dataclass
class User:
    username: str
    password_hash: str
    favorite_player: str
    team_flair: str
    #birthday: str
    joined_date: str
    first_name: str
    last_name: str
    country: str
    comments: List[str]



    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def is_anonymous():
        return False

    def get_id(self):
        return self.username

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    @staticmethod
    def check_password(password_hash, password):
        return check_password_hash(password_hash, password)


@login_manager.user_loader
def load_user(username):
    u = users.find_one({"username": username})
    if not u:
        return None
    return User(username=u["username"])
