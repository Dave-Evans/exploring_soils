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

pull_ipaddress () {
    # For pull public ip address from output of describe
    # Takes filename of JSON as arg
    local ipaddress=$(jq -r '.Reservations[0].Instances[0].NetworkInterfaces[0].Association.PublicIp' $1)
    echo $ipaddress
}

remote_maintenance() {
    # arg is ipaddress
    ssh -i ../wieff_1.pem ubuntu@$1 "sudo apt update -y"
    ssh -i ../wieff_1.pem ubuntu@$1 "sudo apt upgrade -y"
    ssh -i ../wieff_1.pem ubuntu@$1 "sudo reboot"
}

spinup_server () {
    image_id="ami-0fc20dd1da406780b"
    key_name="wieff_1"
    secgrp_id="sg-09832f5ae52230593"
    inst_prof="Arn=arn:aws:iam::392349258765:instance-profile/davemike-test-ec2-role"
    place="AvailabilityZone=us-east-2c"

    out_runinst=$(aws ec2 run-instances --image-id $image_id\
        --count 1\
        --instance-type t2.micro\
        --key-name $key_name\
        --security-group-ids $secgrp_id\
        --iam-instance-profile $inst_prof\
        --placement $place)
    # DEBUG $out_runinst;
    instance_id=$(echo $out_runinst | jq -r '.Instances[0].InstanceId')
    # DEBUG "Instance ID: $instance_id"
    out_filename="out_runinstance.json"
    echo $out_runinst > $out_filename
    # INFO "Output stored in $out_filename"
    echo $out_filename
}

# Backup a file to aws S3
case "$1" in
    deploy)
        # spin up ec2 server
        outfile=$(spinup_server)
        INFO "Output file: $outfile"
        # grab instance id
        instance_id=$(pull_instance_id $outfile)
        # Wait until Running
        aws ec2 wait instance-running --instance-ids $instance_id
        
        describe=$(aws ec2 describe-instances --instance-id $instance_id)
        echo $describe > "describe.json"
        #   and then ip address
        ipaddress=$(pull_ipaddress "describe.json")
        # Basic maintenance
        remote_maintenance $ipaddress
        aws ec2 wait instance-running --instance-ids $instance_id
        # run bootstrap script
        ssh -i ../wieff_1 ubuntu@$ipaddress 'bash -s' < bootstrap.sh
        
        #   including create server specific variables
        ;;
    setcron)
        croncmd="bash /home/ubuntu/exploring_soils/deployment/helper.sh bkup /home/ubuntu/exploring_soils/db.sqlite3"
        cronjob="0 22 * * * $croncmd"
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
esac




