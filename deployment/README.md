# Deployment

This document will serve as my notes for deployment.
The long term goal is I would like to use Terraform to be able to spin up and deploy the necessary infrastructure for this web application. 
This would mean being able to run one or two commands to spin up a tier of the website.

Short term, I will just work on getting it running.

### Basic deployment steps

 - Spinup EC2 (think about which AWS role and how to structure the user)
    - Ubuntu 18.04 LTS `ami-0fc20dd1da406780b`
 - Install necessary software
	- Python
	- modules
	- Webserver
	- Database?
	- Git
	- GDAL

```sh
sudo apt update -y
sudo apt upgrade -y
sudo apt install python3-pip -y
# Install virtual environment
sudo apt-get install -y python3-venv
# Create virtual env
python3 -m venv myvenv
source myvenv/bin/activate

# Git install
# sudo apt install git
# Config, necessary?
git config --global user.name "Dave-Evans"
git config --global user.email "evans.dave.michael@gmail.com"

# Pull in project
git clone https://github.com/Dave-Evans/exploring_soils.git

# Install necessary modules
pip install -r exploring_soils/requirements.txt

# GDAL
sudo apt install gdal-bin

# Install Apache
sudo apt-get install apache2 libapache2-mod-wsgi-py3 -y


```
 - Pull in code
 - Start website?

### Helpful links

[https://www.digitalocean.com/community/tutorials/how-to-serve-django-applications-with-apache-and-mod_wsgi-on-ubuntu-14-04](https://www.digitalocean.com/community/tutorials/how-to-serve-django-applications-with-apache-and-mod_wsgi-on-ubuntu-14-04)

### TODOs:

 - Move the `os.mkdir` in pull_soils.py into a function
 - Turn off debug
 - Hide the security key
 - Hide other stuff using some kind of config from SIBTC
 - Back up script for db.sqlite to S3
 - Force login for entering mileage
 - build bootstrap script
 - commit apache config file
 


