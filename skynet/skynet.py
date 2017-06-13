try:
    # import skynet
    import os

    from flask import Flask, request, session, g, redirect, url_for, abort, \
                      render_template, flash

    from flask_bootstrap import Bootstrap

    from flask_sqlalchemy import SQLAlchemy
except ImportError as err:
    print('Are you run "pip3 install -r requirements.txt in app root dir?"')
    raise err

 # create the application instance :)
app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.from_pyfile('config.py', silent=False)
db = SQLAlchemy(app)
