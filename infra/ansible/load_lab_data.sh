#!/bin/bash

# Enter repository
cd /home/ubuntu/exploring_soils

fl="/home/ubuntu/exploring_soils/data/lab_data_2023.tsv"

# Download survey data form 2020 through 2022
## VARIABLIZE ##
# aws s3 cp s3://davemike-backup-dev/db/wisc_cc_dat.tsv $fl
aws s3 cp s3://$4/db/lab_data_2023.tsv $fl

source myvenv/bin/activate
# Load old survey data to database
# dbname=$1 user=$2 password=$3 fl=$4
python ./infra/ansible/load_lab_data.py $1 $2 $3 $fl

rm -rf ./data/lab_data_2023.tsv