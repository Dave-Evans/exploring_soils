#!/bin/bash

# Enter repository
cd /home/ubuntu/exploring_soils

# Find all migrations directories and delete the contents
# for dr in $(find . -maxdepth 2 -mindepth 1 -type d)
#   do 
#     if [ $(basename $dr) == "migrations" ]
#     then echo $dr
#     sudo rm $dr/* 
#     fi
#   done
find . -maxdepth 3 -path "*/migrations/*.py" -not -name "__init__.py" -delete
# enter virtual env and create fresh migration files,
#   use them to build the database
#   and load data
source myvenv/bin/activate
echo "Making migrations"
python ./manage.py makemigrations
echo "Running migrate"
python ./manage.py migrate
echo "Loading data"
python ./manage.py loaddata data/dump.json
python ./manage.py collectstatic --noinput