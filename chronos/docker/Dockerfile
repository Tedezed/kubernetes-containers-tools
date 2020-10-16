FROM debian:stable
LABEL "MAINTAINER"="Juan Manuel Torres <juanmanuel.torres@aventurabinaria.es>"

ENV MYSQLXPB_PROTOC=/usr/bin/protoc \
    MYSQLXPB_PROTOBUF_INCLUDE_DIR=/usr/include/google/protobuf \
    MYSQLXPB_PROTOBUF_LIB_DIR=/usr/lib/x86_64-linux-gnu \
    DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        wget \
        gnupg \
        cron \
        curl \
        git \
        tree \
        nano \
        procps \
    	rsyslog \
    	apt-transport-https \
        python3.7 \
        python3-pip \
        python3-jinja2 \
        python3-yaml \ 
        python3-websocket \
        python3-jsonpickle \
        python3-httplib2 \
        python3-mysqldb \
        libmariadbclient-dev \
        libprotobuf-dev \
        protobuf-compiler \
        default-mysql-client \
        default-mysql-client-core \
        build-essential \
        autoconf \
        libtool \
        pkg-config \
        python-opengl \
        python-pil \
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
        python3-pyqt4 \
        libgle3 \
        python3-dev \
        python3-setuptools \
        libpq-dev \
    && wget -q https://www.postgresql.org/media/keys/ACCC4CF8.asc -O - | apt-key add - \
    && echo "deb http://apt.postgresql.org/pub/repos/apt/ buster-pgdg main" >> /etc/apt/sources.list \
    && apt-get update && apt-get install postgresql-client-12 -y --force-yes --no-install-recommends \
    && pip3 install --upgrade setuptools wheel \
    && pip3 install psycopg2-binary \
    && pip3 install kubernetes deepdiff psycopg2 mysql-connector \
    && pip3 install google-api-python-client setuptools \
    && pip3 install google-auth google-auth-httplib2 psycopg2-binary psutil passlib \
    # Clean
    && apt-get remove --purge -y \
        build-essential \
        autoconf \
        libtool \
        pkg-config \
        python3-opengl \
        python3-imaging \
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
        python3-pyqt4 \
        libgle3 \
        python3-dev \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get autoclean -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get autoremove -y

# Mode 0 > DEBUG
# Mode 1 > Backup
# Mode 2 > Snapshot
# Mode 3 > Backup + Snapshot

ENV DAYS_TO_DROP=15 \
    DAYS_TO_DROP_SNAPSHOT=3 \
    TIME="10 0 * * *" \
    MODE="all" \
    CONF_MODE="api" \
    PROJECT="project-name-test" \
    ZONE="europe-west1-b" \
    EMAIL_MODE="OFF" \
    PYTHONIOENCODING="UTF-8" \
    GCLOUD_DEFAULT_CREDENTIALS="True" \
    GCLOUD_SA_FILE="/secrets/sa/sa-gcloud.json"

ADD chronos/ /chronos
ADD files/docker-entrypoint.sh /usr/local/bin/

RUN chmod +rx /usr/local/bin/docker-entrypoint.sh /chronos/main.py /chronos/start

USER root
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["/bin/bash"]