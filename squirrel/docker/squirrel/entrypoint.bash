#!/bin/bash
set -e

rm -rf /squirrel/away/

python3 -u /squirrel/main.py mode=$MODE
