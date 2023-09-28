#!/bin/bash
# 1st arg is tier
# Enter repository
cd /home/ubuntu/exploring_soils

ipaddress=$(curl ifconfig.me)

if [ $1 == 'prod' ]; then
    sed -i "s/ALLOWED_HOSTS=.*/ALLOWED_HOSTS=$ipaddress,evansgeospatial.com,www.evansgeospatial.com/g" .env
    sed -i "s/CSRF_TRUSTED_ORIGINS=.*/CSRF_TRUSTED_ORIGINS=https:\/\/evansgeospatial.com,https:\/\/www.evansgeospatial.com/g" .env
else
    sed -i "s/ALLOWED_HOSTS=.*/ALLOWED_HOSTS=$ipaddress,$1.evansgeospatial.com/g" .env
    sed -i "s/CSRF_TRUSTED_ORIGINS=.*/CSRF_TRUSTED_ORIGINS=https:\/\/$1.evansgeospatial.com/g" .env
fi