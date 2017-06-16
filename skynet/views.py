import logging
import sqlalchemy
from flask import current_app
from flask_login import login_user
from wtforms import StringField, BooleanField, PasswordField, FieldList, TextField, TextAreaField, SelectField, validators, FileField
from wtforms.validators import DataRequired, Length, URL, EqualTo, Email
from flask.ext.wtf import Form
from skynet.models import *
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import flask_admin as admin


class ReusableForm(Form):
    username = TextField('User name:', validators=[validators.required()])
    password = TextField('Password:', validators=[validators.required(), validators.Length(min=3, max=35)])
    name = TextField('Your name:', validators=[validators.required()])
    second_name = TextField('Second name:', validators=[validators.Length(min=3, max=35)])
    nick = TextField('Nick:')
    city = TextField('City:', validators=[validators.required(), validators.Length(min=2, max=35)])
    role = TextField('Role:', default='user')

    def reset(self):
        from werkzeug.datastructures import MultiDict
        blankData = MultiDict([('csrf', self.reset_csrf())])
        self.process(blankData)


@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))


@app.before_request
def before_request():
    g.user = current_user


@app.route('/')
def root():
    if not session.get('logged_in'):
        return redirect(url_for('sign_up'))
    else:
        username = session.get('username')
        return redirect(url_for('user', username=username))



@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username = username).first()
    # if user == None:
    #     flash('User ' + username + ' not found.')
    #     return redirect(url_for('login'))
    posts = Post.query.filter_by(user_id=user.id).all()
    return render_template('mypage.html',
        user=user,
        posts=posts)


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
        name = request.form['name']
        second_name = request.form['second_name']
        nick = request.form['nick']
        city = request.form['city']

        app.logger.debug('data accepted')
        msg = User(username, password, name, second_name, nick, city, role='user')
    
        app.logger.debug('db commiting')
        try:
            db.session.add(msg)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            flash('Error: ' + 'user ' + username + ' Already exists')
            return render_template('sign_up.html', error=error)
        app.logger.debug('success')
        if form.validate():
            # for i in User.query.filter_by(username=username).all():
            #     if username == i.username:
            #         flash('Error: ' + username + 'Already exists')
            # Save the comment here.
            session['logged_in'] = True
            flash('Hello ' + username)
            return redirect(url_for('user', username=username))
        else:
            flash('Error: All the form fields are required. ')
            
        session['username'] = username
        # app.logger.debug('user {} successfully login'.format(session.get('username')))
    return render_template('sign_up.html', error=error)


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
            user = user_inf
            login_user(user, force=True)
            app.logger.debug('we are logged in as {}'.format(session.get('username')))
            return redirect(url_for('user', username = username))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    app.logger.debug('we are logged out')
    logout_user()
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
