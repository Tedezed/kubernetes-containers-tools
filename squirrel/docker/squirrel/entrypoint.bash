#!/bin/bash
set -e

rm -rf /squirrel/away/

sleep infinity
python3 -u /squirrel/main.py mode=$MODE
