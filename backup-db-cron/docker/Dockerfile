FROM debian:stable
MAINTAINER Juan Manuel Torres <juanmanuel.torres@aventurabinaria.es>

## ----- PYTHON ----- ##

ENV MYSQLXPB_PROTOC=/usr/bin/protoc \
 MYSQLXPB_PROTOBUF_INCLUDE_DIR=/usr/include/google/protobuf \
 MYSQLXPB_PROTOBUF_LIB_DIR=/usr/lib/x86_64-linux-gnu

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
    python-httplib2 \
    python-mysqldb \
    libmariadbclient-dev \
    libprotobuf-dev \
    protobuf-compiler \
    mysql-client

RUN apt-get install -y \
    build-essential \
    autoconf \
    libtool \
    pkg-config \
    python-opengl \
    python-imaging \
    python-pyrex \
    python-pyside.qtopengl \
    idle-python2.7 \
    qt4-dev-tools \
    qt4-designer \
    libqtgui4 \
    libqtcore4 \
    libqt4-xml \
    libqt4-test \
    libqt4-script \
    libqt4-network \
    libqt4-dbus \
    python-qt4 \
    python-qt4-gl \
    libgle3 \
    python-dev \
    python-setuptools

RUN pip install kubernetes deepdiff psycopg2 mysql-connector \
    && pip install google-api-python-client
RUN pip install google-auth google-auth-httplib2 psycopg2-binary

RUN apt-get remove --purge -y \
    build-essential \
    autoconf \
    libtool \
    pkg-config \
    python-opengl \
    python-imaging \
    python-pyrex \
    python-pyside.qtopengl \
    idle-python2.7 \
    qt4-dev-tools \
    qt4-designer \
    libqtgui4 \
    libqtcore4 \
    libqt4-xml \
    libqt4-test \
    libqt4-script \
    libqt4-network \
    libqt4-dbus \
    python-qt4 \
    python-qt4-gl \
    libgle3 \
    python-dev \
    && rm -rf /var/lib/apt/lists/*

## ----- ENV ----- ##

ENV DAYS_TO_DROP=15 \
    DAYS_TO_DROP_SNAPSHOT=3 \
    TIME="10 12 * * *"

# Mode 0 > DEBUG
# Mode 1 > Backup
# Mode 2 > Snapshot
# Mode 3 > Backup + Snapshot

ENV MODE="1" \
    CONF_MODE="conf-map" \
    PROJECT="project-name-test" \
    ZONE="europe-west1-b"

## ----- END ----- ##

ADD slug-backup-db-cron/ /slug-backup-db-cron
ADD files/docker-entrypoint.sh /usr/local/bin/

RUN chmod +rx /usr/local/bin/docker-entrypoint.sh /slug-backup-db-cron/main.py /slug-backup-db-cron/start

USER root
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["/bin/bash"]