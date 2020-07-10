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
aws s3 cp s3://davemike-backup/db/db.sqlite3 ./db.sqlite3

# Replace apache config file
sudo cp ./deployment/000-default.conf /etc/apache2/sites-available/000-default.conf

chmod 664 db.sqlite3
sudo chown :www-data db.sqlite3
sudo chown :www-data ~/exploring_soils
sudo service apache2 restart

bash ./deployment/helper.sh setcron
bash ./deployment/helper.sh setcron




