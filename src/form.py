from flask_wtf import FlaskForm, Form
from wtforms import (
    PasswordField,
    StringField,
    SubmitField,
    SelectField,
    DateField,
    BooleanField,
)
from wtforms.validators import DataRequired, Email, ValidationError, InputRequired
from src.mongo import users_col
from src.resources.user import load_user
from src.sql import get_player_names, get_team_names, get_league_names


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class SignupForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    birthday = DateField("Birthday", validators=[DataRequired()])
    terms = BooleanField(
        "I agree to the Terms and Conditions", validators=[DataRequired()]
    )

    submit = SubmitField("Sign up")

    def validate_username(self, username: StringField):
        user = load_user(username.data)

        if user is not None:
            raise ValidationError("Please use a different username.")


class SearchForm(Form):
    search_type = SelectField(
        "Search Type", choices=[("Team", "Team"), ("Player", "Player")]
    )
    search_text = StringField("Search Text")

    sort_type = SelectField(
        "Sort by...",
        choices=[("", "Sort by..."), ("Team", "Team"), ("Player", "Player"), ("League", "League")],
        validators=[InputRequired()],
        
    )

    league = SelectField("League")
    team = SelectField("Team")
    # player = SelectField("Player")

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)

        leagues = [("", "Leagues")]
        leagues.extend(zip(get_league_names(), get_league_names()))
        self.league.choices = leagues
        # self.league.data = "Leagues"

        teams = [("", "Teams")]
        teams.extend(zip(get_team_names(), get_team_names()))
        self.team.choices = teams
        # self.team.data = "Teams"

        # teams = [("", "Players")]
        # teams.extend(zip(get_player_names(), get_player_names()))
        # self.player.choices = teams
