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

function do_test(){
  # install pytest
  pip install pytest
  local path="$1"
  if [ -z "$path" ]; then
    path=app/tests
  fi
  echo "testing $path"
  pytest "$path"
}

while [[ $# -gt 0 ]]
do
  key="$1"
  value="$2"
  case $key in
    -s|--start)
      wait_db
      upgrade_alembic
      start
      exit 0
      ;;
    -m|--migrate)
      wait_db
      upgrade_alembic
      do_migration "$value"
      exit 0
      ;;
    -t|--test)
      wait_db
      upgrade_alembic
      do_test "$value"
      exit 0
      ;;
    *)
      echo "Unknown option $1"
      exit 1
      ;;
  esac
done