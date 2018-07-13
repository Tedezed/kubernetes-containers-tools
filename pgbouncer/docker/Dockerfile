FROM debian:9
MAINTAINER Juan Manuel Torres <juanmanuel.torres@aventurabinaria.es>

RUN apt-get update \
    && apt-get install -y \
        nano \
        pgbouncer \
        postgresql-client-9.6 \
        postgresql-client-common

#VOLUME /files/users
EXPOSE 5432

ADD files /files
RUN chmod +x /files/bin/start.sh

ENV PG_SERVICE_NAME="localhost" \
    PG_SERVICE_PORT="5432" \
    PG_USERNAME="demo" \
    PG_PASSWORD="demo" \
    DB_NAME="test" \
    CONFDIR="/tmp" \
    DIR_CONFDIR="tmp" \
    PG_ADMIN="admin" \
    PG_PORT="5432" \
    POOL_MODE="transaction"\
    MAX_CON="500" \
    DEFAULT_POOL_SIZE="60" \
    MIN_POOL_SIZE="10"

USER daemon

CMD ["/files/bin/start.sh"]