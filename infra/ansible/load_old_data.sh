#!/bin/bash

# Enter repository
cd /home/ubuntu/exploring_soils

fl="/home/ubuntu/exploring_soils/data/wisc_cc_dat.tsv"

# Download survey data form 2020 through 2022
## VARIABLIZE ##
# aws s3 cp s3://davemike-backup-dev/db/wisc_cc_dat.tsv $fl
aws s3 cp s3://$4/db/wisc_cc_dat.tsv $fl

source myvenv/bin/activate
# Load old survey data to database
# dbname=$1 user=$2 password=$3 fl=$4
python ./infra/ansible/load_table_to_db.py $1 $2 $3 $fl

rm -rf ./data/wiscs_cc_dat.tsv

