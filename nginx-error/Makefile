#!make

CONTAINER_REPO:=tedezed
CONTAINER_IMAGE:=nginx-error
CONTAINER_VERSION:=latest
SUPPORT_EMAIL:="devops@guadaltech.es"
TEAM_NAME:="DevOps Team"

build:
	docker build -f Dockerfile -t ${CONTAINER_REPO}/${CONTAINER_IMAGE}:${CONTAINER_VERSION} \
	--build-arg SUPPORT_EMAIL=${SUPPORT_EMAIL} \
	--build-arg TEAM_NAME=${TEAM_NAME} \
	.

build-no-cache:
	docker build -f Dockerfile -t ${CONTAINER_REPO}/${CONTAINER_IMAGE}:${CONTAINER_VERSION} --no-cache \
	--build-arg SUPPORT_EMAIL=${SUPPORT_EMAIL} \
	--build-arg TEAM_NAME=${TEAM_NAME} \
	.

push:
	docker push ${CONTAINER_REPO}/${CONTAINER_IMAGE}:${CONTAINER_VERSION}

gcloud-push:
	gcloud docker -- push ${CONTAINER_REPO}/${CONTAINER_IMAGE}:${CONTAINER_VERSION}

all: build

