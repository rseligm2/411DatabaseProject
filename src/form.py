from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, SelectField, DateField, BooleanField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class SignupForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    birthday = DateField("Birthday", validators=[DataRequired()])
    terms = BooleanField("I agree to the Terms and Conditions", validators=[DataRequired()])

    submit = SubmitField("Sign up")
