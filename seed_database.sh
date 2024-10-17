#!/bin/bash

rm db.sqlite3
rm -rf ./volunteerapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations volunteerapi
python3 manage.py migrate volunteerapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens

