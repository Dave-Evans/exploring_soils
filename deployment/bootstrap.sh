#!/bin/bash


# software install
for _tool in awscli python3-pip python3-venv gdal-bin apache2 libapache2-mod-wsgi-py3 git postgresql postgresql-contrib postgis; do
    echo "Installing ${_tool}"
    sudo apt install ${_tool} -y
done;

# Pull in project code
git clone https://github.com/Dave-Evans/exploring_soils.git
cd exploring_soils
git config --global user.name "Dave-Evans"
git config --global user.email "evans.dave.michael@gmail.com"

# Create virtual env
python3 -m venv myvenv
source myvenv/bin/activate

# Install necessary python modules
pip3 install -r requirements.txt

# Pull database info from S3
# aws s3 cp s3://davemike-backup/db/db.sqlite3 ./db.sqlite3
mkdir ./data
aws s3 cp s3://davemike-backup/db/dump.json ./data/dump.json

# Set up database
# First grab user name from uploaded .env file
local database_url=$(grep -e '^DATABASE_URL' .env | sed 's/DATABASE_URL=//')
# Splitting the database url into components
CONN=(${database_url//:/ })
# Grabbing the username portion and stripping off forward slashes
local db_username=$(echo ${CONN[1]} | sed -e 's/\/\///')
# Grabbing name of database by stripping off port digits and forward slash
local db_name=$(echo ${CONN[3]} | sed -e 's/[0-9]*//' | sed -e 's/\///')
# Grabbing password by grabbing everying before @
local db_pass=$(${CONN[2]} | sed 's/@.*//')

CREATE DATABASE db_davemike;
CREATE USER usr_davemike;
ALTER USER usr_davemike WITH PASSWORD '';
ALTER DATABASE db_davemike OWNER TO usr_davemike;

# Build tables 
`python ./manage.py migrate`

# Load data
`python manage.py loaddata ./data/dump.json`

# Replace apache config file
sudo cp ./deployment/000-default.conf /etc/apache2/sites-available/000-default.conf

# chmod 664 db.sqlite3
# sudo chown :www-data db.sqlite3
sudo chown :www-data ~/exploring_soils
sudo service apache2 restart

bash ./deployment/helper.sh setcron
bash ./deployment/helper.sh setcron




