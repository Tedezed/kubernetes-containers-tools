#!make

# Base
SHELL:=/bin/bash

# Local conf
USER_LOCAL:=`whoami`


build:
	docker build -f Dockerfile -t tedezed/nagios:latest .

push:
	docker push tedezed/nagios:latest

run:
	docker run -p 8888:80 -e NAGIOS_PASS="nagios" -t tedezed/nagios:latest

start:
	sudo chgrp ${USER_LOCAL} -R volumes
	sudo chmod 770 -R volumes
	docker-compose -f local.yaml up

drop:
	../../tools/docker/drop-docker.sh 