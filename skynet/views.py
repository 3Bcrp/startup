import logging
import sqlalchemy
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug import *
from skynet.forms import *
from skynet.models import *
# from skynet.config import ALLOWED_EXTENSIONS


@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))


@app.before_request
def before_request():
    g.user = current_user

#######################################################
#                                                     #
#                    USER PAGES                       #
#                                                     #
#######################################################

@app.route('/')
@login_required
def root():
    username = session.get('username')
    return redirect(url_for('user', username=username))


@app.route('/user/<username>')
@login_required
def user(username):
    form = AddPostForm(request.form)
    user = User.query.filter_by(username = username).first()
    posts = Post.query.filter_by(user_id=user.id).all()
    return render_template('mypage.html',
                           form=form,
                           user=user,
                           posts=posts)

#######################################################
#                                                     #
#                   USER METHODS                      #
#                                                     #
#######################################################

########### PHOTOS ##############
@app.route('/user/<username>/photos', methods=['GET', 'POST'])
@login_required
def photos(username):
    form = AddAlbumForm(request.form)
    user = User.query.filter_by(username = username).first()
    if request.method == "POST" :
        if form.validate():
            title = request.form['title']
            album_inf = Album(title=title,
                              date=datetime.datetime.now(),
                              user_id=current_user.id)
    
            try:
                current_user.album.append(album_inf)
                basedir = os.path.dirname(os.path.abspath(__file__))
                album_path = os.path.join(basedir,
                                           app.config['STATIC_FOLDER'],
                                           app.config['UPLOAD_FOLDER'],
                                           username,
                                           app.config['PHOTO_ALBUMS_FOLDER'],
                                           title)
                os.mkdir(album_path)
                db.session.commit()
                flash('New album created')
                app.logger.debug('new album created added')
            except Exception as err:
                flash('Error occured')
                app.logger.debug('Error occured: %s' % err)
        else:
            flash('Error: incorrect data input')
            app.logger.debug('Posting validations error')
    albums = Album.query.filter_by(user_id=user.id).all()
    return render_template('photos.html', user=user, albums=albums, form=form)



@app.route('/user_search', methods=[ 'POST', 'GET'])
@login_required
def user_search():
    app.logger.debug('user_search method called')
    # search_form = UserSearchForm(request.form)
    if request.method == "POST" :
        app.logger.debug('user_search validating')
        if search_form.validate_on_submit():
            search_user = request.form['user-search']
            app.logger.debug('searching user  %s' % search_user)
    
            users = User.query.filter_by(username = search_user).all()
    
            return render_template('user_search.html', users=users)
        else:
            app.logger.debug('Search validation falling')
    return redirect('/')


@app.route('/add_post', methods=['POST'])
@login_required
def add_post():
    form = AddPostForm(request.form)
    if form.validate():
        current_user = User.query.filter_by(username = session.get('username')).first()
        title = request.form['title']
        text = request.form['text']
        post_inf = Post(title=title,
                        text=text,
                        date=datetime.datetime.now(),
                        user_id=current_user.id)
    
        current_user.post.append(post_inf)
    
        db.session.commit()
    
        flash('New entry was successfully posted')
        app.logger.debug('new info added')
    else:
        flash('Error: incorrect data input')
        app.logger.debug('Posting validations error')
    
    return redirect(url_for('user', username=session.get('username')))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/user/<username>/settings', methods=['GET', 'POST'])
@login_required
def settings(username):
    user = g.user
    form = SettingsForm(request.form)
    if request.method == 'POST':
        password = request.form['password']
        nick = request.form['nick']
        city = request.form['city']
        if 'file' not in request.files:
            flash('No file part')
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            basedir = os.path.dirname(os.path.abspath(__file__))
            avatar_path = os.path.join(basedir,
                                       app.config['STATIC_FOLDER'],
                                       app.config['UPLOAD_FOLDER'],
                                       username,
                                       app.config['PHOTO_ALBUMS_FOLDER'],
                                       app.config['AVATAR_FOLDER'],
                                       filename)
            file.save(avatar_path)

            user.nick = nick
            user.password = password
            user.city = city
            user.avatar = os.path.relpath(avatar_path, start='./skynet/static/')
            db.session.commit()
            
            return redirect(url_for('user', username=g.user.username))
    return render_template('settings.html', user=user, username=user.username, form=form)

#######################################################
#                                                     #
#                     AUTH BLOCK                      #
#                                                     #
#######################################################

@app.route("/sign_up", methods=['GET', 'POST'])
def sign_up():
    error = None
    form = SignUpForm(request.form)
    if request.method == 'POST':
        app.logger.debug('sign_up POST method')
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        second_name = request.form['second_name']
        nick = request.form['nick']
        city = request.form['city']
        app.logger.debug('start validation {}'.format(request.form))

        if form.validate_on_submit():
            # for i in User.query.filter_by(username=username).all():
            #     if username == i.username:
            #         flash('Error: ' + username + 'Already exists')
            # Save the comment here.
            try:
                # User uploading folder creation
                basedir = os.path.dirname(os.path.abspath(__file__))
                user_path = os.path.join(basedir,
                                         app.config['STATIC_FOLDER'],
                                         app.config['UPLOAD_FOLDER'],
                                         username)
                avatar = os.path.relpath(os.path.join(basedir,
                                                      app.config['STATIC_FOLDER'],
                                                      app.config['DEFAULT_FOLDER'],
                                                      app.config['DEFAULT_AVATAR']),
                                         start='./skynet/static/')
            
                app.logger.debug('data accepted')
                msg = User(username=username, password=password,
                   name=name, second_name=second_name,
                   nick=nick, city=city, role='user',
                   avatar=avatar)

                app.logger.debug('db commiting')
                db.session.add(msg)
                os.mkdir(user_path)
                os.mkdir(os.path.join(user_path,
                                      app.config['PHOTO_ALBUMS_FOLDER']))
                os.mkdir(os.path.join(user_path,
                                      app.config['PHOTO_ALBUMS_FOLDER'],
                                      app.config['AVATAR_FOLDER']))
                db.session.commit()
                app.logger.debug('success')
                session['logged_in'] = True
                session['username'] = username
                flash('Hello ' + username)
                g.user = msg
                login_user(g.user, force=True)
                return redirect(url_for('root'))
            except Exception as err:
                flash('Error: ' + 'user ' + username + ' already exists')
                app.logger.debug('Error occured: %s' % err)
        else:
            app.logger.debug('sign up validation falling')
            flash('Error: All the form fields are required. ')
            
        session['username'] = username
        # app.logger.debug('user {} successfully login'.format(session.get('username')))
    return render_template('sign_up.html', form=form, error=error)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm(request.form)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if form.validate_on_submit():
            try:
                user_inf = User.query.filter_by(username=username).first()
                session['logged_in'] = True
                session['username'] = username
                flash('You were logged in')
                user = user_inf
                login_user(user, force=True)
                app.logger.debug('we are logged in as {}'.format(session.get('username')))
                return redirect(url_for('root', username = username))
            except Exception as err:
                flash('Login error')
                app.logger.debug('Error occured: %s' % err)

        else:
            app.logger.debug('Login validation exception: {}, {}'.format(username, password))
            flash('Error: Please type correct data in fields!')
    return render_template('login.html', form=form, error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    app.logger.debug('we are logged out')
    logout_user()
    return redirect(url_for('login'))

#######################################################
#                                                     #
#               LOGGER SETTING UP                     #
#                                                     #
#######################################################

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
