
build:
	docker build -f Dockerfile-centos -t tedezed/pgpool-centos:latest .

build-debian:
	docker build -f Dockerfile-debian -t tedezed/pgpool-debian:latest .

push:
	docker push tedezed/pgpool-centos:latest

push-debian:
	docker push tedezed/pgpool-debian:latest

all:
	docker build -f Dockerfile-centos -t tedezed/pgpool-centos:latest .
	docker push tedezed/pgpool-centos:latest
