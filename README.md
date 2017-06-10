SKYNET - A NEW AGE SOCIAL NETWORK
=================================

# Why?

Because we can.

# How to start

* install docker-engine
* run `./.start.sh version_from_repository`

for example: `./.start.sh development`

# Under the hood

We use:
* python3
* flask
* flask-admin
* sqlalchemy
* postgresql 9.6

`docker-compose` form and start postgres docker container

`models.py` make a migration to skynet_db

`runserver.py` start app and connect it to postgres
