from skynet import *
from skynet.models import *

from wtforms import Form, TextField
from wtforms import validators

import datetime

from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash, Markup
from flask_admin import *

from flask_login import login_required, login_user

import logging
from logging.handlers import RotatingFileHandler


class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])
    password = TextField('Password:', validators=[validators.required(), validators.Length(min=3, max=35)])

    def reset(self):
        from werkzeug.datastructures import MultiDict
        blankData = MultiDict([('csrf', self.reset_csrf())])
        self.process(blankData)


@app.route('/')
def root():
    if not session.get('logged_in'):
        return redirect(url_for('sign_up'))
    else:
        username = session.get('username')
        return redirect(url_for('user', username=username))


@app.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username = username).first()
    if user == None:
        flash('User ' + username + ' not found.')
        return redirect(url_for('login'))
    posts = Post.query.filter_by(user_id = user.id).all()
    return render_template('mypage.html',
        user = user,
        posts = posts)


@app.route('/photos')
def photos():
    return render_template('photos.html')



@app.route("/sign_up", methods=['GET', 'POST'])
def sign_up():
    error = None
    
    form = ReusableForm(request.form)
    if request.method == 'POST':
        app.logger.debug('sign_up POST method')
        username = request.form['username']
        password = request.form['password']
        
        app.logger.debug('data accepted')
        msg = User(username, password)
    
        app.logger.debug('db commiting')
        db.session.add(msg)
        db.session.commit()
        
        app.logger.debug('success')
        if form.validate():
            # Save the comment here.
            session['logged_in'] = True
            flash('Hello ' + username)
        else:
            flash('Error: All the form fields are required. ')
            
        session['username'] = username
        app.logger.debug('user {} successfully login'.format(session.get('username')))
        return redirect(url_for('user', username=username))
    return render_template('sign_up.html', error=error)


@app.route('/add', methods=['POST'])
def add_post():
    if not session.get('logged_in'):
        abort(401)

    title = request.form['title']
    text = request.form['text']
    date = datetime.datetime.now()
    
    msg = Post(title, text,date)
    
    db.session.add(msg)
    db.session.commit()

    flash('New entry was successfully posted')
    app.logger.debug('new info added')
    return redirect(url_for('show_posts'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user_inf = User.query.filter_by(username=username).first()

        if user_inf is None:
            error = 'Invalid username'
            app.logger.debug('invalid uname'.format())
        elif password != user_inf.password:
            error = 'Invalid password'
            app.logger.debug('invalid pswd')
        else:
            session['logged_in'] = True
            session['username'] = username
            flash('You were logged in')
            app.logger.debug('we are logged in as {}'.format(session.get('username')))
            return redirect(url_for('user', username = username))

    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    app.logger.debug('we are logged out')
    return redirect(url_for('login'))


# Setup the logger
file_handler = logging.FileHandler('skynet/logs/apperror.log')
handler = logging.StreamHandler()
file_handler.setLevel(logging.DEBUG)
handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
))
handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
))
app.logger.addHandler(handler)
app.logger.addHandler(file_handler)
