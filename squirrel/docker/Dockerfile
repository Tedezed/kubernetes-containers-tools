FROM python:3.7.3-slim-stretch
MAINTAINER Juan Manuel Torres <juanmanuel.torres@aventurabinaria.es>

ENV MODE="controller"

RUN apt-get update \
	&& apt-get install -y gcc gpg\
	&& pip3 install kubernetes gnupg

ADD squirrel /squirrel

#ENTRYPOINT ["python3", "-u", "/squirrel/main.py", "mode=controller"]
ENTRYPOINT ["sleep", "infinity"]