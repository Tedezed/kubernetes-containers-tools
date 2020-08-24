#FROM python:3.5-slim-stretch
FROM debian:stretch-slim
MAINTAINER Juan Manuel Torres <juanmanuel.torres@aventurabinaria.es>

# Modes: controller or cronjob
ENV MODE="cronjob" \
	DEBUG="False"

RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
		curl \
		make \
		gcc \
		gpg \
		nano \
		python3.5 \
		python3-gnupg \
		python3-pip \
		python3-setuptools \
		libpq-dev \
		python3-dev procps \
	&& pip3 install wheel

## && curl -SL https://gnupg.org/ftp/gcrypt/gnupg/gnupg-1.4.20.tar.bz2 -o gnupg-2.1.18.tar.bz2 \
##	&& tar xjf gnupg-2.1.18.tar.bz2 \

ADD squirrel /squirrel

# RUN pip3 install \
# 		kubernetes==10.0.1 \
# 		psycopg2-binary==2.8.3 \
# 		psycopg2==2.8.3 \
# 		passlib==1.7.1 \
# 		pyperclip==1.7.0 \
# 		python-gnupg==0.3.9

RUN mkdir -p /squirrel_certs \
	&& pip3 install -r /squirrel/requirements.txt && pip3 freeze \
	&& chmod +x /squirrel/entrypoint.bash

ENTRYPOINT ["/squirrel/entrypoint.bash"]
#ENTRYPOINT ["sleep", "infinity"]