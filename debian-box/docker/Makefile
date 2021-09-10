#!make

# Base
SHELL:=/bin/bash

# Local conf
USER_LOCAL:=`whoami`


build-8:
	docker build -f Dockerfile-8 -t tedezed/debian-box:8 .

push-8:
	docker push tedezed/debian-box:8

build-slim:
	docker build -f Dockerfile-slim -t tedezed/debian-box:slim .

push-slim:
	docker push tedezed/debian-box:slim

build:
	docker build -f Dockerfile-latest -t tedezed/debian-box:latest .

push:
	docker push tedezed/debian-box:latest

drop:
	../../tools/docker/drop-docker.sh 
