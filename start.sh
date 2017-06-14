#!/usr/bin/env bash
status_handler() {
    if [ "$?" = "0" ]; then
        echo "DONE"
    else
        echo "FAIL" 1>&2
        exit 1
    fi
}


echo "Type the version to start, followed by [ENTER]:"
read version

git checkout $version
status_handler

docker-compose up -d
status_handler

pip3 install -r requirements.txt
status_handler

echo "Start migration..."
python3 skynet/models.py
status_handler

echo "Run server"
python3 runserver.py
status_handler