try:
    # import skynet
    import os

    from flask import Flask, request, session, g, redirect, url_for, abort, \
                      render_template, flash

    from flask_bootstrap import Bootstrap
    from flask_login import LoginManager
    from flask_sqlalchemy import SQLAlchemy
    from flask_wtf import CSRFProtect
except ImportError as err:
    print('Are you run "pip3 install -r requirements.txt in app root dir?"')
    raise err


csrf = CSRFProtect()
 # create the application instance :)
app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.from_pyfile('config.py', silent=False)
csrf.init_app(app)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
