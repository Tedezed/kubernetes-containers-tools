
CONTAINER_REPO:=tedezed
CONTAINER_IMAGE:=pgpool-centos-ha
CONTAINER_VERSION:=latest

build:
	docker build -f Dockerfile-centos -t ${CONTAINER_REPO}/${CONTAINER_IMAGE}:${CONTAINER_VERSION} .

push:
	docker push ${CONTAINER_REPO}/${CONTAINER_IMAGE}:${CONTAINER_VERSION}

all:
	docker build -f Dockerfile-centos -t ${CONTAINER_REPO}/${CONTAINER_IMAGE}:${CONTAINER_VERSION} .
	docker push ${CONTAINER_REPO}/${CONTAINER_IMAGE}:${CONTAINER_VERSION}
