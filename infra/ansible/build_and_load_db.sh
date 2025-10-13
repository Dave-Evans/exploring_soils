#!/bin/bash
# First arg is backup s3 bucket

# Enter repository
cd /home/ubuntu/exploring_soils

# Download data
# get all s3 files
rslt=$(aws s3 ls $1/db/)

# get all backup files with dates
# Sorted to get biggest date, most recent
bkups=$( echo $rslt | grep -o "dump_\([0-9]\)\{8\}\.json" | sort -r)

# Grab the first, most recent
fl_bkup=$( echo $bkups | cut -d " " -f 1 )

aws s3 cp s3://$1/db/$fl_bkup ./data/.

bkup_fl="dump_$(printf '%(%Y%m%d)T\n' -1).json"

# find . -maxdepth 3 -path "*/migrations/*.py" -not -name "__init__.py" -delete
# enter virtual env and create fresh migration files,
#   use them to build the database
#   and load data
source myvenv/bin/activate
echo "Checking out working state"
git checkout d3aa27aec4ec38a3af6b746251df6d4e14f63726
echo "Making migrations"
python ./manage.py makemigrations
echo "Running migrate"
python ./manage.py migrate
echo "Back to update todate"
git switch -
echo "Making migrations, again"
python ./manage.py makemigrations
echo "Running migrate, again"
python ./manage.py migrate
echo "...migrations for glccp, why?"
python ./manage.py makemigrations glccp
python ./manage.py migrate glccp
echo "Loading data"
python ./manage.py loaddata data/$fl_bkup
python ./manage.py collectstatic --noinput