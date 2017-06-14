import os
import os.path as op

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import flask_admin as admin
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import filters

from wtforms import validators
try:
    from skynet.skynet import *
except:
    from skynet import *


# Create models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80), unique=True)
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def __str__(self):
        return self.username


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime)

    user_id = db.Column(db.Integer(), db.ForeignKey(User.id))
    user = db.relationship(User, backref='posts')

    def __init__(self, title, text, date):
        self.title = title
        self.text = text
        self.date = date

    def __str__(self):
        return self.title


# Customized User model admin
class UserAdmin(sqla.ModelView):
    inline_models = ()

# Create M2M table
post_tags_table = db.Table('post_tags', db.Model.metadata,
                           db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
                           )


# Create admin
admin = admin.Admin(app, name='Skynet: admin', template_mode='bootstrap3')

# Add views
admin.add_view(UserAdmin(User, db.session))
admin.add_view(UserAdmin(Post, db.session))

if __name__ == '__main__':
    # Make migration
    db.create_all()
