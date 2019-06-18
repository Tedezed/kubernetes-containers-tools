FROM python:3.7-slim-stretch
MAINTAINER Juan Manuel Torres <juanmanuel.torres@aventurabinaria.es>

ENV MODE="controller"

RUN apt-get update \
	&& apt-get install -y gcc gpg nano \
	&& pip3 install kubernetes gnupg

ADD squirrel /squirrel
RUN chmod +x /squirrel/entrypoint.bash

ENTRYPOINT ["/squirrel/entrypoint.bash"]
#ENTRYPOINT ["sleep", "infinity"]