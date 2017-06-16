import os
import os.path as op

from flask import Flask
from flask.ext.login import login_required
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
    password = db.Column(db.String(80), unique=False)
    name = db.Column(db.String(80), unique=False)
    second_name = db.Column(db.String(80), unique=False)
    nick = db.Column(db.String(80), unique=False)
    city = db.Column(db.String(80), unique=False)
    role = db.Column(db.String(7),unique=False, default= 'user')

    def __init__(self, username, password, name, second_name, nick, city, role):
        self.username = username
        self.password = password
        self.name = name
        self.second_name = second_name
        self.nick = nick
        self.city = city
        self.role = role

    def __str__(self):
        return self.username

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


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
    adminUser = User(username='admin', password='1234', name='admin', second_name='adminov', nick='God blessed',
              city='Admin City', role='admin')
    db.session.add(adminUser)
    db.session.commit()