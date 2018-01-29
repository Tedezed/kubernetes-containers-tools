build:
	docker build -f Dockerfile -t tedezed/sftpd-multiuser:latest .

run:
	docker run -d -p 8080:80 tedezed/sftpd-multiuser:latest

drop:
	sh ../tools/docker/drop-docker.sh

push:
	docker push tedezed/sftpd-multiuser:latest

run-debug:
	docker run -p 8080:80 tedezed/sftpd-multiuser:latest