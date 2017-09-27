FROM debian:stable
MAINTAINER Juan Manuel Torres <juanmanuel.torres@aventurabinaria.es>

ENV DAYS_TO_DROP 15
ENV DAYS_TO_DROP_SNAPSHOT 3
ENV TIME "10 12 * * *"

# Mode 0 > DEBUG
# Mode 1 > Backup
# Mode 2 > Snapshot
# Mode 3 > Backup + Snapshot

ENV MODE "0"
ENV PROJECT test
ENV ZONE test

##### PYTHON

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        cron \
        curl \
        git \
        tree \
        nano \
        procps \
    	rsyslog \
    	apt-transport-https \
        postgresql-client-common postgresql-client 

RUN apt-get install -y --no-install-recommends \
    python2.7 \
    python-pip \
    python-jinja2 \
    python-yaml \ 
    python-websocket \
    python-jsonpickle \
    && rm -rf /var/lib/apt/lists/*

RUN pip install kubernetes deepdiff psycopg2
RUN pip install google-api-python-client

##### PYTHON

ADD slug-backup-db-cron/ /slug-backup-db-cron

ADD files/docker-entrypoint.sh /usr/local/bin/
RUN chmod +rx /usr/local/bin/docker-entrypoint.sh /slug-backup-db-cron/main.py /slug-backup-db-cron/start

USER root
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["/bin/bash"]