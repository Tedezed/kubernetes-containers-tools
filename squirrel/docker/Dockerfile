#FROM python:3.5-slim-stretch
FROM debian:stretch-slim
MAINTAINER Juan Manuel Torres <juanmanuel.torres@aventurabinaria.es>

# Modes: controller or cronjob
ENV MODE="cronjob"

RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
		gcc gpg nano python3.5 python3-gnupg python3-pip python3-setuptools libpq-dev python3-dev \
	&& pip3 install wheel \
	&& pip3 install kubernetes psycopg2-binary psycopg2 passlib

ADD squirrel /squirrel
RUN chmod +x /squirrel/entrypoint.bash

ENTRYPOINT ["/squirrel/entrypoint.bash"]
#ENTRYPOINT ["sleep", "infinity"]