from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import InputRequired, Length

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField("Password", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired(), Length(max=50)])
    first_name = StringField("First name", validators=[InputRequired(), Length(max=30)])
    last_name = StringField("Last name", validators=[InputRequired(), Length(max=30)])
    img_url = StringField("Profile Image URL", validators=[Length(max=100)])
    
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=75)])
    password = PasswordField("Password", validators=[InputRequired()])

class SearchForm(FlaskForm):
    title = StringField("Title (Please type in the English name)", validators=[InputRequired(), Length(min=1, max=100)])

