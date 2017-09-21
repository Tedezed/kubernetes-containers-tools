FROM debian:stable-slim
MAINTAINER Juan Manuel Torres <juanmanuel.torres@aventurabinaria.es>

ENV DAYS_TO_DROP 15

##### PYTHON

RUN apt-get update \
    && apt-get install -y \
    	curl \
    	rsyslog \
    	apt-transport-https \
        python2.7 \
        python-pip \
        python-jinja2 \
        git \
        nano \
        procps \
    && rm -rf /var/lib/apt/lists/*

RUN pip install kubernetes deepdiff
##### PYTHON

ADD slug-backup-db-cron/ /slug-backup-db-cron

ADD files/docker-entrypoint.sh /usr/local/bin/
RUN chmod +rx /usr/local/bin/docker-entrypoint.sh

USER root
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["/bin/bash"]