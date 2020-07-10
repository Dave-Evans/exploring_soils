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
# Specify volume? VPC? Placement?
aws ec2 run-instances --image-id ami-0fc20dd1da406780b\
    --count 1\
    --instance-type t2.micro\
    --key-name wieff_1\
    --security-group-ids sg-09832f5ae52230593\
    --iam-instance-profile Arn=arn:aws:iam::392349258765:instance-profile/davemike-test-ec2-role\
    --placement AvailabilityZone=us-east-2c > out_runinstance.json
# Need to parse the output for the Instance ID and then run describe on that instance to get the public IP
InstanceID=$(jq -r '.Instances[0].InstanceId' out_runinstance.json)
aws ec2 describe-instances $InstanceID
```
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

# Install aws cli
sudo apt  install awscli -y


```
 - Pull in code
 - Start website?

### Helpful links

[https://www.digitalocean.com/community/tutorials/how-to-serve-django-applications-with-apache-and-mod_wsgi-on-ubuntu-14-04](https://www.digitalocean.com/community/tutorials/how-to-serve-django-applications-with-apache-and-mod_wsgi-on-ubuntu-14-04)

### TODOs:

 - Move the `os.mkdir` in pull_soils.py into a function
 - Turn off debug
 - ** COMPLETE** Hide the security key
 - ** COMPLETE** Hide other stuff using some kind of config from SIBTC
 - Back up script for db.sqlite to S3
    - Done with helper script and `bash deployment/helper.sh bkup db.sqlite3`
    - schedule with cron:
        - `bash /home/ubuntu/exploring_soils/deployment/helper.sh bkup /home/ubuntu/exploring_soils/db.sqlite3`
 - ** COMPLETE** Force login for entering mileage
 - ** COMPLETE** build bootstrap script
 - ** COMPLETE** commit apache config file
 - Address Github raised vulnerabilities
 
#### Investigate

 - HTTPs?
 - Gnunicorn
 - shift to postgresql
 
 
 aws ec2 run-instances --image-id ami-xxxxxxxx --count 1 --instance-type t2.micro --key-name MyKeyPair --security-group-ids sg-903004f8 --subnet-id subnet-6e7f829e
 


