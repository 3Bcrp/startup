from skynet import *
from skynet.models import *

from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash, Markup
from flask_admin import *

import logging
from logging.handlers import RotatingFileHandler


@app.route('/')
def show_posts():
    posts = Post.query.all()
    app.logger.debug('we are in the root')
    return render_template('show_posts.html', posts=posts)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)

    title = request.form['title']
    text = request.form['text']

    db.session.add(Post(title, text))
    db.session.commit()

    flash('New entry was successfully posted')
    app.logger.debug('new info added')
    return redirect(url_for('show_posts'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
            app.logger.debug('invalid uname')
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
            app.logger.debug('invalid pswd')
        else:
            session['logged_in'] = True
            flash('You were logged in')
            app.logger.debug('we are logged in')
            return redirect(url_for('show_posts'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    app.logger.debug('we are logged out')
    return redirect(url_for('show_entries'))


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
