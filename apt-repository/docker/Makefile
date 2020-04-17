#!make

CONTAINER_REPO:=tedezed
CONTAINER_IMAGE:=apt-repository
CONTAINER_VERSION:=latest

build:
	docker build -f Dockerfile -t ${CONTAINER_REPO}/${CONTAINER_IMAGE}:${CONTAINER_VERSION} .

push:
	docker push ${CONTAINER_REPO}/${CONTAINER_IMAGE}:${CONTAINER_VERSION}

gcloud-push:
	gcloud docker -- push ${CONTAINER_REPO}/${CONTAINER_IMAGE}:${CONTAINER_VERSION}

build-no-cache:
	docker build -f Dockerfile -t ${CONTAINER_REPO}/${CONTAINER_IMAGE}:${CONTAINER_VERSION} --no-cache .

save:
	docker save ${CONTAINER_REPO}/${CONTAINER_IMAGE}:${CONTAINER_VERSION} -o ${CONTAINER_IMAGE}-${CONTAINER_VERSION}.docker

all: build

