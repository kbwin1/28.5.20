from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,EmailField
from wtforms.validators import InputRequired, Length


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(max=20)])
    password = PasswordField("Password", validators=[InputRequired()])
    email = EmailField("email", validators=[InputRequired(), Length(max=50)])
    first_name = StringField("First name", validators=[InputRequired(), Length(max=30)])
    last_name = StringField("Last name", validators=[InputRequired(), Length(max=30)])


class LogingForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class FeedbackForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired(), Length(max=100)])
    content = StringField("Content", validators=[InputRequired()])

