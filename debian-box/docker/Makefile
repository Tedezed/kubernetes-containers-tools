#!make

# Base
SHELL:=/bin/bash

# Local conf
USER_LOCAL:=`whoami`


build-8:
	docker build -f Dockerfile-8 -t tedezed/debian-box:8 .

push-8:
	docker push tedezed/debian-box:8

drop:
	../../tools/docker/drop-docker.sh 