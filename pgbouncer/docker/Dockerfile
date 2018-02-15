FROM debian:9
MAINTAINER Juan Manuel Torres <juanmanuel.torres@aventurabinaria.es>

RUN apt-get update \
    && apt-get install -y \
        nano \
        pgbouncer

VOLUME /files/users
EXPOSE 5432

ADD files /files
RUN chmod +x /files/bin/start.sh

ENV PG_SERVICE_NAME="localhost" \
    PG_SERVICE_PORT="5432" \
    DB_NAME="test" \
    CONFDIR="/tmp" \
    PG_ADMIN="admin" \
    PG_PORT="6543"

USER daemon

CMD ["/files/bin/start.sh"]