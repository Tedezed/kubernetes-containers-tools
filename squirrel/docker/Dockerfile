#FROM python:3.5-slim-stretch
FROM debian:stretch-slim
MAINTAINER Juan Manuel Torres <juanmanuel.torres@aventurabinaria.es>

ENV MODE="controller"

#RUN sleep 999999999

RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
		gcc gpg nano python3.5 python3-gnupg python3-pip python3-setuptools \
	&& pip3 install wheel \
	&& pip3 install kubernetes

ADD squirrel /squirrel
RUN chmod +x /squirrel/entrypoint.bash

ENTRYPOINT ["/squirrel/entrypoint.bash"]
#ENTRYPOINT ["sleep", "infinity"]