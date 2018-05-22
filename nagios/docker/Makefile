
build:
	docker build -f Dockerfile -t tedezed/nagios:latest .

push:
	docker push tedezed/nagios:latest

run:
	docker run -p 8080:80 -e NAGIOS_PASS="demo" -t tedezed/nagios:latest

drop:
	../../tools/docker/drop-docker.sh 