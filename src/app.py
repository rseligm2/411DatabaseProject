import secrets

from flask import Flask
from flask_login import LoginManager


app = Flask(__name__)
login_manager = LoginManager(app)
app.secret_key = secrets.token_urlsafe(24)

import src.form
import src.routes

if __name__ == "__main__":
    app.run(debug=True)
