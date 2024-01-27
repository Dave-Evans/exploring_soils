#!/bin/bash

# Enter repository
cd /home/ubuntu/exploring_soils

fl_biomass="/home/ubuntu/exploring_soils/data/bn05905_p_cover_crop2023_biomass.csv"
fl_forage="/home/ubuntu/exploring_soils/data/dairyland_labs_forage_analysis_data_2023.csv"

# Download survey data form 2020 through 2022
## VARIABLIZE ##
# aws s3 cp s3://davemike-backup-dev/db/wisc_cc_dat.tsv $fl
aws s3 cp s3://$4/db/$(basename $fl_biomass) $fl_biomass
aws s3 cp s3://$4/db/$(basename $fl_forage) $fl_forage

source myvenv/bin/activate
# Load old survey data to database
# dbname=$1 user=$2 password=$3 fl=$4
python ./infra/ansible/load_lab_data.py $1 $2 $3 $fl_biomass
python ./infra/ansible/load_lab_data.py $1 $2 $3 $fl_forage

rm -rf $fl_biomass 
rm -rf $fl_forage