from skynet import app
from skynet.skynet import *
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, Markup
from flask_admin import *
import logging
from logging.handlers import RotatingFileHandler


@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('select title, text from entries order by id desc')
    entries = cur.fetchall()
    app.logger.debug('we are in the root')
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into entries (title, text) values (?, ?)',
                [request.form['title'], request.form['text']])
    db.commit()
    flash('New entry was successfully posted')
    app.logger.debug('new info added')
    return redirect(url_for('show_entries'))


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
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    app.logger.debug('we are logged out')
    return redirect(url_for('show_entries'))

#Setup the logger
file_handler = logging.FileHandler('logs/apperror.log')
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
