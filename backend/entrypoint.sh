#!/bin/bash

# Define default values for the arguments
arg1=default1
arg2=default2
arg3=default3

# Parse the arguments from the command line

function wait_db(){
  echo "waiting for db"
  while !</dev/tcp/database/5432;
      do sleep 1;
  done;
}

function upgrade_alembic(){
  echo "updating db"
  alembic upgrade head
}

function start(){
  echo "starting server"
  uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
}

function do_migration(){
  echo "migrating"
  alembic revision --autogenerate -m "$1"
}

while [[ $# -gt 0 ]]
do
  key="$1"
  case $key in
    -s|--start)
      wait_db
      upgrade_alembic
      start
      shift
      ;;
    -m|--migrate)
      wait_db
      do_migration "$2"
      shift
      ;;
  esac
done