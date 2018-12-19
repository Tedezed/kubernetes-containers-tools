SHELL := /bin/bash

build:
	docker build -f Dockerfile -t ${NAME_REGISTRY}/${NAME_IMAGE}:${VERSION_IMAGE} .

build-no-cache:
	docker build -f Dockerfile --no-cache -t ${NAME_REGISTRY}/${NAME_IMAGE}:${VERSION_IMAGE} .

push:
	gcloud docker -- push ${NAME_REGISTRY}/${NAME_IMAGE}:${VERSION_IMAGE}

all: build push

default: all
