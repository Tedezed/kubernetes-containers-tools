SHELL := /bin/bash

build:
	docker build -f Dockerfile -t ${NAME_REGISTRY}/${NAME_IMAGE}:${VERSION_IMAGE} .

build-no-cache:
	docker build -f Dockerfile -t ${NAME_REGISTRY}/${NAME_IMAGE}:${VERSION_IMAGE} --no-cache .

save:
	docker save ${NAME_REGISTRY}/${NAME_IMAGE}:${VERSION_IMAGE} -o ${NAME_IMAGE}-${VERSION_IMAGE}.docker

run:
	docker run -e RELAYHOST=${RELAYHOST} -e RELAYHOST_PORT=${RELAYHOST_PORT} \
	-e SMTP_KEY=${SMTP_KEY} -e SMTP_SECRET=${SMTP_SECRET} -e HOSTNAME=${HOSTNAME} \
	-t ${NAME_REGISTRY}/${NAME_IMAGE}:${VERSION_IMAGE}

push:
	#gcloud docker -- push ${NAME_REGISTRY}/${NAME_IMAGE}:${VERSION_IMAGE}
	docker push ${NAME_REGISTRY}/${NAME_IMAGE}:${VERSION_IMAGE}

all: build push

default: all
