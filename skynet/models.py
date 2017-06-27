import os
import os.path as op

from flask import Flask
from flask_login import login_required
from flask_sqlalchemy import SQLAlchemy
import flask_admin as admin
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import filters

import datetime

from wtforms import validators
try:
    from skynet.skynet import *
except:
    from skynet import *


# Create models
class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80), unique=False)
    name = db.Column(db.String(80), unique=False)
    second_name = db.Column(db.String(80), unique=False)
    nick = db.Column(db.String(80), unique=False)
    city = db.Column(db.String(80), unique=False)
    role = db.Column(db.String(7),unique=False, default= 'user')
    user_path = db.Column(db.String(120))
    avatar = db.Column(db.String(180))
    
    post = db.relationship("Post", backref="user", lazy="dynamic")
    album = db.relationship("Album", backref="user", lazy="dynamic")
    photo = db.relationship("Photo", backref="user", lazy="dynamic")

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


class Album(db.Model):
    __tablename__ = 'album'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    title = db.Column(db.String(120))
    photo = db.relationship("Photo", backref="album", lazy="dynamic")
    
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    
    
class Photo(db.Model):
    __tablename__ = 'photo'
    
    id = db.Column(db.Integer, primary_key=True)
    photo_name = db.Column(db.String(80))
    date = db.Column(db.DateTime)
    title = db.Column(db.String(120))
    likes = db.Column(db.Integer)
    latitude = db.Column(db.Float)
    longtitude = db.Column(db.Float)
    album_id = db.Column(db.Integer(), db.ForeignKey('album.id'))
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))


class Post(db.Model):
    __tablename__ = 'post'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))


# Customized User model admin
class UserAdmin(sqla.ModelView):
    inline_models = ()

# Create M2M table
# post_tags_table = db.Table('post_tags', db.Model.metadata,
#                           db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
#                           )

# Create admin
admin = admin.Admin(app, name='Skynet: admin', template_mode='bootstrap3')
# Add views
admin.add_view(UserAdmin(User, db.session))
admin.add_view(UserAdmin(Post, db.session))
admin.add_view(UserAdmin(Album, db.session))
admin.add_view(UserAdmin(Photo, db.session))

if __name__ == '__main__':
    # Make migration
    db.create_all()
    adminUser = User(username='admin', password='1234',
                     name='admin', second_name='adminov',
                     nick='God blessed', city='Admin City',
                     role='admin', avatar='default/default-avatar.jpg')
    db.session.add(adminUser)
    db.session.commit()