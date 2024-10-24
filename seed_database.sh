#!/bin/bash

rm db.sqlite3
rm -rf ./volunteerapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations volunteerapi
python3 manage.py migrate volunteerapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata organizations
python3 manage.py loaddata skills
python3 manage.py loaddata opportunities
python3 manage.py loaddata volunteers
python3 manage.py loaddata volunteeropportunities