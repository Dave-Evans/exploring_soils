#!/bin/bash

# Enter repository
cd /home/ubuntu/exploring_soils

# Download county data gdb
mkdir ./data/county_nrcs_a_mn.gdb
mkdir ./data/county_nrcs_a_wi.gdb

aws s3 cp s3://$4/db/county_nrcs_a_mn.gdb/ ./data/county_nrcs_a_mn.gdb --recursive
aws s3 cp s3://$4/db/county_nrcs_a_wi.gdb/ ./data/county_nrcs_a_wi.gdb --recursive
# Load county data to database
# ogr2ogr -overwrite -f PostgreSQL PG:"host=localhost dbname=db_davemike user=usr_davemike password=luggage12543" -t_srs EPSG:4326 -nln mn_counties ./data/county_nrcs_a_mn.gdb county_nrcs_a_mn
ogr2ogr -overwrite -f PostgreSQL PG:"host=localhost dbname=$1 user=$2 password=$3" -t_srs EPSG:4326 -nln mn_counties ./data/county_nrcs_a_mn.gdb county_nrcs_a_mn
ogr2ogr -overwrite -f PostgreSQL PG:"host=localhost dbname=$1 user=$2 password=$3" -t_srs EPSG:4326 -nln wi_counties ./data/county_nrcs_a_wi.gdb county_nrcs_a_wi

rm -rf ./data/county_nrcs_a_mn.gdb
rm -rf ./data/county_nrcs_a_wi.gdb