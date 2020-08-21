#!/bin/bash
set -e

rm -rf /squirrel/away/

python3 -u /squirrel/main.py mode=$MODE

if [ "$DEBUG" != "False" ]; then
    for i in $(ls /squirrel_certs); do  
        echo /squirrel_certs/$i
        cat /squirrel_certs/$i
    done
fi
