#!/bin/bash

set -e
set -o pipefail

# Copy bash logger code to simplify install for now:
#--------------------------------------------------------------------------------------------------
# Bash Logger
# Copyright (c) Dean Rather
# Licensed under the MIT license
# http://github.com/deanrather/bash-logger
#--------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------
# Configurables

export LOGFILE=/dev/null
export LOG_FORMAT='%DATE [%LEVEL] %MESSAGE'
export LOG_DATE_FORMAT='+%FT%T.000Z'                # Eg: 2014-09-07T21:51:57.000Z
export LOG_COLOR_DEBUG="\033[0;37m"                 # Gray
export LOG_COLOR_INFO="\033[0m"                     # White
export LOG_COLOR_NOTICE="\033[1;32m"                # Green
export LOG_COLOR_WARNING="\033[1;33m"               # Yellow
export LOG_COLOR_ERROR="\033[1;31m"                 # Red
export LOG_COLOR_CRITICAL="\033[44m"                # Blue Background
export LOG_COLOR_ALERT="\033[43m"                   # Yellow Background
export LOG_COLOR_EMERGENCY="\033[41m"               # Red Background
export RESET_COLOR="\033[0m"

#--------------------------------------------------------------------------------------------------
# Individual Log Functions
# These can be overwritten to provide custom behavior for different log levels

DEBUG()     { LOG_HANDLER_DEFAULT "$FUNCNAME" "$@"; }
INFO()      { LOG_HANDLER_DEFAULT "$FUNCNAME" "$@"; }
NOTICE()    { LOG_HANDLER_DEFAULT "$FUNCNAME" "$@"; }
WARNING()   { LOG_HANDLER_DEFAULT "$FUNCNAME" "$@"; }
ERROR()     { LOG_HANDLER_DEFAULT "$FUNCNAME" "$@"; exit 1; }
CRITICAL()  { LOG_HANDLER_DEFAULT "$FUNCNAME" "$@"; exit 1; }
ALERT()     { LOG_HANDLER_DEFAULT "$FUNCNAME" "$@"; exit 1; }
EMERGENCY() { LOG_HANDLER_DEFAULT "$FUNCNAME" "$@"; exit 1; }

#--------------------------------------------------------------------------------------------------
# Helper Functions

# Outputs a log formatted using the LOG_FORMAT and DATE_FORMAT configurables
# Usage: FORMAT_LOG <log level> <log message>
# Eg: FORMAT_LOG CRITICAL "My critical log"
FORMAT_LOG() {
  local level="$1"
  local log="$2"
  local pid=$$
  local date="$(date -u "$LOG_DATE_FORMAT")"
  local formatted_log="$LOG_FORMAT"
  formatted_log="${formatted_log/'%MESSAGE'/$log}"
  formatted_log="${formatted_log/'%LEVEL'/$level}"
  formatted_log="${formatted_log/'%PID'/$pid}"
  formatted_log="${formatted_log/'%DATE'/$date}"
  echo "$formatted_log\n"
}

# Calls one of the individual log functions
# Usage: LOG <log level> <log message>
# Eg: LOG INFO "My info log"
LOG() {
  local level="$1"
  local log="$2"
  local log_function_name="${!level}"
  $log_function_name "$log"
}

#--------------------------------------------------------------------------------------------------
# Log Handlers

# All log levels call this handler (by default...), so this is a great place to put any standard
# logging behavior
# Usage: LOG_HANDLER_DEFAULT <log level> <log message>
# Eg: LOG_HANDLER_DEFAULT DEBUG "My debug log"
LOG_HANDLER_DEFAULT() {
  # $1 - level
  # $2 - message
  local formatted_log="$(FORMAT_LOG "$@")"
  LOG_HANDLER_COLORTERM "$1" "$formatted_log"
  # LOG_HANDLER_LOGFILE "$1" "$formatted_log"
}

# Outputs a log to the stdout, colourised using the LOG_COLOR configurables
# Usage: LOG_HANDLER_COLORTERM <log level> <log message>
# Eg: LOG_HANDLER_COLORTERM CRITICAL "My critical log"
LOG_HANDLER_COLORTERM() {
  local level="$1"
  local log="$2"
  local color_variable="LOG_COLOR_$level"
  local color="${!color_variable}"
  [[ -t 1 ]] && [[ -t 2 ]] && log="$color$log$RESET_COLOR"
  echo -en "$log"
}

# Appends a log to the configured logfile
# Usage: LOG_HANDLER_LOGFILE <log level> <log message>
# Eg: LOG_HANDLER_LOGFILE NOTICE "My critical log"
LOG_HANDLER_LOGFILE() {
  local level="$1"
  local log="$2"
  local log_path="$(dirname "$LOGFILE")"
  [ -d "$log_path" ] || mkdir -p "$log_path"
  echo "$log" >> "$LOGFILE"
}

# TODO: 
#   Make remote_maintenance and bootstrap so they don't end the script
#   Do this with subshells and while loops to grep the pid?
# Global variables...for now

top_level=$(git rev-parse --show-toplevel)

image_id="ami-0fc20dd1da406780b"
key_name="wieff_1"
secgrp_id="sg-09832f5ae52230593"
inst_prof="Arn=arn:aws:iam::392349258765:instance-profile/davemike-test-ec2-role"
place="AvailabilityZone=us-east-2c"

env_file="$top_level/.env"
key_file="$top_level/$key_name.pem"



create_tag () {
    
    #InstanceID=$(jq -r '.Instances[0].InstanceId' out_runinstance.json)
    InstanceID=$1
    Key=$2
    Value=$3
    aws ec2 create-tags --resources $InstanceID --tags Key=$Key,Value=$Value

}


pull_instance_id () {
    # For pull instance ID from output of run-instances
    # Takes filename of JSON as arg
    local instance_id=$(jq -r '.Instances[0].InstanceId' $1)
    echo $instance_id
    #INFO "Instance ID: $instance_id"
}

pull_instance_status () {
    # Pull status
    # Takes filename of JSON as arg
    local status=$(jq -r '.Reservations[0].Instances[0].State.Name' $1)
    echo $status

}

pull_ipaddress () {
    # For pull public ip address from output of describe
    # Takes filename of JSON as arg
    # I would like to expand this to also return the publicdnsname, how to use a default arg?
    if [ $# -eq 1 ] || [ $2 == ip ]
        then 
            local result=$(jq -r '.Reservations[0].Instances[0].NetworkInterfaces[0].Association.PublicIp' $1)
    elif [ $2 == dns ]
        then 
            local result=$(jq -r '.Reservations[0].Instances[0].NetworkInterfaces[0].Association.PublicDnsName' $1)
    else
        printf "arg must be 'ip', 'dns', or none"
        # exit 1
    fi
    echo $result
}

remote_maintenance() {
    # arg 1 is ipaddress
    # arg 2 is key file
    # arg 3 is optional and is whether to reboot
    ssh -t -i $1 ubuntu@$2 "sudo apt update -y"
    ssh -t -i $1 ubuntu@$2 "sudo apt upgrade -y"
    
    if [ $3 == 'restart' ]
        then
            ssh -t -i $1 ubuntu@$2 "sudo reboot"
    fi
            
}

run_bootstrap() {
    ssh -i $key_file ubuntu@$ipaddress 'bash -s' < bootstrap.sh
}

spinup_server () {
    # $1 image_id="ami-0fc20dd1da406780b"
    # $2 key_name="wieff_1"
    # $3 secgrp_id="sg-09832f5ae52230593"
    # $4 inst_prof="Arn=arn:aws:iam::392349258765:instance-profile/davemike-test-ec2-role"
    # $5 place="AvailabilityZone=us-east-2c"
    # $6 out_runinsts="out_runinstance.json"
    
    output=$(aws ec2 run-instances --image-id $1\
        --count 1\
        --instance-type t2.micro\
        --key-name $2\
        --security-group-ids $3\
        --iam-instance-profile $4\
        --placement $5)
    instance_id=$(echo $output | jq -r '.Instances[0].InstanceId')
    echo $output > $6
}

create_env_file() {

    local ipaddress=$(pull_ipaddress $out_describe ip)
    local pubdns=$(pull_ipaddress $out_describe dns)
    local secret_key=$(grep -e 'SECRET_KEY' $env_file | sed 's/SECRET_KEY=//')
    local debug='False'
    local allowed_hosts="$ipaddress,$pubdns"
    local database_url='sqlite:////home/ubuntu/exploring_soils/db.sqlite3'
    echo -e "SECRET_KEY=$secret_key\nDEBUG=$debug\nALLOWED_HOSTS=$allowed_hosts\nDATABASE_URL=$database_url" > remote.env
    echo remote.env

}

scp_to_server() {
    # first arg is src
    # second is dst
    scp -i $key_file $1 ubuntu@$ipaddress:$2

}

# Backup a file to aws S3
branchname=$2
out_runinsts="$top_level/deployment/out_runinstance_$branchname.json"
out_describe="$top_level/deployment/describe_$branchname.json"
        
case "$1" in
    spinup)

        INFO "Looking at branch $branchname"
        b_spinup=true
        # Currently just handling the case when its still running
        if [ -a $out_runinsts ]
            then
                instance_id=$(pull_instance_id $out_runinsts)        
                describe=$(aws ec2 describe-instances --instance-id $instance_id)
                echo $describe > $out_describe
                status=$(pull_instance_status $out_describe)
                
                if [ $status == running ]
                    then             
                        INFO "Instance $instance_id is currently running"
                        b_spinup=false
                fi
        fi    
        # spin up ec2 server
        if [ $b_spinup == true ]
            then
                INFO "Spinning up EC2 Server"
                spinup_server $image_id $key_name $secgrp_id $inst_prof $place $out_runinsts      
        fi

        INFO "Output file: $out_runinsts"

        instance_id=$(pull_instance_id $out_runinsts)
        INFO "Instance ID: $instance_id"

        INFO "Waiting until instance is running..."
        aws ec2 wait instance-running --instance-ids $instance_id
        
        INFO "Running describe on instance..."
        describe=$(aws ec2 describe-instances --instance-id $instance_id)
        echo $describe > $out_describe
        INFO "Stored in $out_describe"
        
        #   get ip address
        ipaddress=$(pull_ipaddress $out_describe)

        INFO "Running maintenance, updates and upgrades..."
        remote_maintenance $key_file $ipaddress
        
        INFO "Restarting instance..."
        remote_maintenance $key_file $ipaddress restart
        aws ec2 wait instance-running --instance-ids $instance_id
        # Make this a separate function so that it doesn't end the flow
        INFO "Running bootstrap.sh..."
        # run_bootstrap
        INFO "Bootstrapping complete."        
        # Create remote.env file
        remote_env=$(create_env_file)
        # scp to server as .env 
        scp_to_server $remote_env '~/exploring_soils/.env'
        
        INFO "Creating tags..."
        create_tag $instance_id "tier" "prod"
        create_tag $instance_id "branch" $branchname
        ;;
    opensite)
        ipaddress=$(pull_ipaddress $out_describe ip)
        python -mwebbrowser http://$ipaddress
        ;;
    ssh)
        ipaddress=$(pull_ipaddress $out_describe ip)
        INFO "ssh'ing into server at $ipaddress"
        ssh -i $key_file ubuntu@$ipaddress
        ;;        
    maintenance)
        INFO "Restarting instance..."
        ipaddress=$(pull_ipaddress $out_describe ip)
        remote_maintenance $key_file $ipaddress restart
        aws ec2 wait instance-running --instance-ids $instance_id
        INFO "Additional commands"
        INFO "Additional commands."
        WARNING "Additional commands."
        ;;
    setcron)
        croncmd="bash /home/ubuntu/exploring_soils/deployment/helper.sh bkup /home/ubuntu/exploring_soils/db.sqlite3"
        cronjob="52 00 * * * $croncmd"
        INFO "Creating cronjob:"
        INFO "$cronjob"
        ( crontab -l | grep -v -F "$croncmd" ; echo "$cronjob" ) | crontab -
        ;;
    bkup)
        bucket="davemike-backup"
        folder="db"
        file=$(basename -- "$2")
        INFO "Copying $2'"
        INFO "To 's3://$bucket/$folder/$file'"
        aws s3 cp "$2" "s3://$bucket/$folder/$file"
        ;;
    *)
        ERROR "Usage: bash helper.sh spinup|opensite|ssh|setcron|bkup"
        exit 1        
        ;;
esac




