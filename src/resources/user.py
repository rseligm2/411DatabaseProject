from dataclasses import *
from typing import *
from datetime import datetime

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
from src.mongo import users_col

login_manager.login_view = "login"


@dataclass
class User:
    _id: str
    username: str
    password_hash: str
    birthday: datetime
    email: str
    comments: List[str]
    team_flair: Optional[str] = None
    favorite_player: Optional[str] = None

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

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


    def __repr__(self) -> str:
        return f"User(<username: {self.username}, password_hash: {self.password_hash}>)"


@login_manager.user_loader
def load_user(username):
    u = users_col.find_one({"username": username})
    if not u:
        return None
    # print(u)
    return User(**u)
