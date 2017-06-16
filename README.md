SKYNET - A NEW AGE SOCIAL NETWORK
=================================

# Why?

Because we can.

# How to start

* install docker-engine
* run `./start.sh`
* type `version_to_checkout`

for example: 

`$ ./.start.sh`

`$ master`

# Under the hood

We use:
* python 3.6
* flask
* flask-admin
* sqlalchemy
* postgresql 9.6

`docker-compose` form and start postgres docker container

`models.py` make a migration to skynet_db

`runserver.py` start app and connect it to postgres

# Troobleshoting

Requirements dependencies install falling:
* check python version (must be 3.6)

Migration falling down:
* `$ docker-compose down`
* `$ docker-compose up -d`
