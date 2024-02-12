#!/bin/bash

# Enter repository
cd /home/ubuntu/exploring_soils

fl_labdata_2023="/home/ubuntu/exploring_soils/data/all_lab_data_2023.tsv"

# Download survey data form 2020 through 2022
## VARIABLIZE ##
# aws s3 cp s3://davemike-backup-dev/db/wisc_cc_dat.tsv $fl
aws s3 cp s3://$4/db/lab_data_2023/$(basename $fl_labdata_2023) $fl_labdata_2023

source myvenv/bin/activate
# Load old survey data to database
# dbname=$1 user=$2 password=$3 fl=$4
python ./infra/ansible/load_lab_data.py $1 $2 $3 $fl_labdata_2023

rm -rf $fl_labdata_2023