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

# Helper to pull variabls from .env file
extract_envvar () { 
    local caps=$(echo ${1^^})
    grep -e "^$caps" $env_file | sed "s/$caps=//"
}

# Making a wrapper around terraform output ip
# in case future versions of this don't use terraform for ip
pullip () {
    terraform output ip
}

# Directory
top_level=$(git rev-parse --show-toplevel)
# Branch name
branchname=$(git symbolic-ref --short HEAD)
# Default .env file
env_file="$top_level/.env"
# Default virtual env
myvenv_dir="$top_level/myvenv"

# Actions 
# infra: terraform
# helper.sh infra pathto.envfile
# - create terraform.tfvars file from envfile
# - run terraform
# - pull ip address out and add back to envfile

# deploy: ansible
# helper.sh deploy pathto.envfile
# - create hosts file
# - create vars/main.yml file
# - run ansible



# Terraform variables file, assume it doesn't exist and replace
#   prompt for deletion in future?
tfvars=$top_level/infra/terraform.tfvars
ansvars=$top_level/infra/ansible/vars/main.yml
anshosts=$top_level/infra/ansible/hosts

create_tf_vars () {

    if [ -f "$tfvars" ]; then
        WARNING "$tfvars already exists."
        echo "This will be overwritten. Enter 'yes' to proceed"
        read resp
        if [ "$resp" != 'yes' ]; then
            echo $resp
            exit 1
        fi
        rm $tfvars
    fi

    INFO "Creating Terraform variables file: $tfvars"
    for _var in aws_storage_bucket_name key_name aws_access_key_id aws_secret_access_key; do
        eval "$_var=$(extract_envvar $_var)"
        eval "_val=\${$_var}"
        if [ -z "$_val" ]; then
            ERROR "need to specify '$_var' in $env_file"
            # echo "need to specify '$_var' in $env_file"
        else
            DEBUG "$_var: $_val"
            # echo "$_var: $_val"
            echo "$_var = \"$_val\"" >> $tfvars
        fi
    done

}

create_ansible_vars() {

    if [ -f "$ansvars" ]; then
        WARNING "$ansvars already exists."
        echo "This will be overwritten. Enter 'yes' to proceed"
        read resp
        if [ "$resp" != 'yes' ]; then
            echo $resp
            exit 1
        fi
        rm $ansvars
    else
        # Check for ansible/vars
        if [ ! -d $(dirname $ansvars) ]; then
            # create if not
            mkdir $(dirname $ansvars)
        fi
    fi

    INFO "Creating Ansible variables file: $ansvars"
    for _var in database_user database_name database_pass key_name; do
        eval "$_var=$(extract_envvar $_var)"
        eval "_val=\${$_var}"
        if [ -z "$_val" ]; then
            ERROR "need to specify '$_var' in $env_file"
            # echo "need to specify '$_var' in $env_file"
        else
            DEBUG "$_var: $_val"
            # echo "$_var: $_val"
            echo "$_var: $_val" >> $ansvars
        fi
    done

}

spinup_infra () {
    
    INFO "Creating infrastructure..."
    terraform apply

    INFO "Extracting IP Address"
    ipaddress=$( pullip )
    sed -i "s/ALLOWED_HOSTS=.*/ALLOWED_HOSTS=$ipaddress/g" $env_file

}

create_ansible_hostsfile () {

    # Deletes hosts by default

    # Check for ansible/vars
    if [ ! -d $(dirname $anshosts) ]; then
        # create if not
        mkdir $(dirname $anshosts)
    fi

    INFO "Creating hosts file"
    # Create hosts
    echo "$( pullip ) ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/$(extract_envvar key_name).pem" > $anshosts    
}

provision_deploy () {
    INFO "Provisioning database components"
    ansible-playbook -i ./ansible/hosts ./ansible/database.yml
    # must be run after db is setup
    INFO "Provisioning web components and deploying application"
    ansible-playbook -i ./ansible/hosts ./ansible/website.yml
    INFO "Updating servers"
    ansible-playbook -i ./ansible/hosts ./ansible/update.yml
}

scp_to_server() {
    # first arg is src
    # second is dst
    scp -i $key_file $1 ubuntu@$ipaddress:$2

}

dump_db() {
    # For dumping the database as backup
    source $myvenv_dir/bin/activate
    python $top_level/manage.py dumpdata --indent 4 --natural-primary --natural-foreign --traceback > ./data/dump.json
    deactivate
}
while [ -n "$1" ]; do
    case "$1" in

        -f) # Catch the option for a different environment file
            if [ ! -f $2 ]; then
                echo "Option -b specifies an alternate env file."
                echo "$2 is not a file"
                exit 1
            fi
            echo "Resetting default environment file to $2"
            env_file="$2"

            shift
            ;;        
        create_vars)
            # Create Terraform vars file
            create_tf_vars
            # Create Ansible vars file
            create_ansible_vars
            ;;
        spinup_infra)
            spinup_infra
            # Here: if prod attach elastic ip address
            # Grab that ip and add to env file and use in hosts
            #   Add a switch to pullip function, if prod then use elastic ip
            # Populate hosts
            create_ansible_hostsfile        
            ;;
        deploy)
            # Run Ansible
            provision_deploy
            ;;
        teardown)
            terraform destroy
            ;;            
        opensite)
            ipaddress=$( pullip )
            python -mwebbrowser http://$ipaddress
            ;;
        ssh)
            ipaddress=$( pullip )
            key_name=$(extract_envvar key_name)
            INFO "ssh'ing into server at $ipaddress"
            ssh -i "~/.ssh/$key_name.pem" ubuntu@$ipaddress
            ;;      
        maintenance)
            ansible-playbook -i ./ansible/hosts ./ansible/update.yml
            ;;
        dumpdb)
            INFO "Dumping database to ./data/dump.json"
            dump_db
            ;;
        bkup)
            bucket=$(extract_envvar AWS_STORAGE_BUCKET_NAME)
            folder="db"
            file=$(basename -- "$2")
            INFO "Copying $2'"
            INFO "To 's3://$bucket/$folder/$file'"
            aws s3 cp "$2" "s3://$bucket/$folder/$file"
            shift
            ;;
        *)
            ERROR "Usage: bash helper.sh create_vars|spinup_infra|teardown|deploy|ssh|opensite|dumpdb|bkup"
            exit 1        
            ;;
    esac
    shift
done




