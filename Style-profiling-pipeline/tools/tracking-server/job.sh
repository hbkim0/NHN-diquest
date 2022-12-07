#!/bin/bash


if [ $1 = "clean" ]
then
    fuser -k -n tcp 5002
    python mysql.py clean
    sudo rm -rf /style_profiling/mamihlapinatapai/tracking-server
elif [ $1 = 'make' ]
then
    python mysql.py create
    cd /style_profiling/mamihlapinatapai/
    mlflow server --backend-store-uri mysql+pymysql://diquest:ek2znptm2@133.186.171.5:3306/mamihlapinatapai --default-artifact-root ./tracking-server -p 5002 --host 133.186.171.5
fi