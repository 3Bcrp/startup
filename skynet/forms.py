from flask import current_app
from skynet import *
from wtforms import StringField, BooleanField, PasswordField, FieldList, TextField, TextAreaField, SelectField, validators, FileField
from wtforms.validators import DataRequired, Length, URL, EqualTo, Email
from flask_wtf import FlaskForm

class MainForm(FlaskForm):
    
    def reset(self):
        from werkzeug.datastructures import MultiDict
        blankData = MultiDict([('csrf', self.reset_csrf())])
        self.process(blankData)

class SignUpForm(MainForm):
    username = TextField('User name:', [validators.DataRequired(), validators.Length(min=3, max=35)])
    password = TextField('Password:', [validators.DataRequired(), validators.Length(min=3, max=35)])
    name = TextField('Your name:', [validators.DataRequired(), validators.Length(min=1, max=35)])
    second_name = TextField('Second name:', [validators.DataRequired(), validators.Length(min=3, max=35)])
    nick = TextField('Nick:')
    city = TextField('City:', validators=[validators.DataRequired(), validators.Length(min=2, max=35)])


class LoginForm(MainForm):
    username = TextField('User name:', [validators.DataRequired(), validators.Length(min=3, max=35)])
    password = TextField('Password:', [validators.DataRequired(), validators.Length(min=3, max=35)])


class AddPostForm(MainForm):
    title = TextField('Post title:', [validators.DataRequired(), validators.Length(min=1, max=35)])
    text = TextField('Post text:', [validators.DataRequired(), validators.Length(min=1, max=35)])       


class UserSearchForm(MainForm):
    user_search = TextField('User name:', [validators.DataRequired(), validators.Length(min=1, max=35)])     
