# default settings
SECRET_KEY = '123456790'
USERNAME = 'test'
PASSWORD = 'test'

# postgresql settings
POSTGRESQL_DATABASE_DATABASE = 'skynet_db'
POSTGRESQL_DATABASE_USERNAME = 'skynet_admin'
POSTGRESQL_DATABASE_PASSWORD = 'skynet_pass'
POSTGRESQL_DATABASE_HOSTNAME = 'localhost'
POSTGRESQL_DATABASE_PORTNUMB = '5432'

# SQLAlchemy connection string
SQLALCHEMY_DATABASE_URI = 'postgresql://{usrn}:{pasw}@{host}:{port}/{db_n}'.format(
    usrn=POSTGRESQL_DATABASE_USERNAME,
    pasw=POSTGRESQL_DATABASE_PASSWORD,
    host=POSTGRESQL_DATABASE_HOSTNAME,
    port=POSTGRESQL_DATABASE_PORTNUMB,
    db_n=POSTGRESQL_DATABASE_DATABASE)

# SQLAlchemy settings
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True
DEBUG = True