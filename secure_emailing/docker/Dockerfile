FROM python:2.7
MAINTAINER Juan Manuel Torres <juanmanuel.torres@aventurabinaria.es>

ENV DEBIAN_FRONTEND="noninteractive" \
	PORT="1025" \
	REMOTE_HOST="192.168.1.23" \
	REMOTE_PORT="2525" \
	NETWORKS="0.0.0.0/0" \
	DB_HOST="postgres" \
	DB_PORT="5432" \
	DB_NAME="emailing" \
	DB_USER="emailing" \
	PGPASSWORD="PASS" \
	DEBUG="False"

ADD common/ /mnt/common
RUN chmod +x /mnt/common/executable/bash/entrypoint.sh \
	&& apt-get update \
	&& apt-get install python-pip postgresql-client nano -y \
	&& pip install psycopg2 psycopg2-binary \
	&& ln -s /mnt/common/smtp_proxy_v2/mailadmin /usr/bin/mailadmin \
	&& chmod +x /usr/bin/mailadmin \
	&& echo "source /mnt/common/smtp_proxy_v2/completion_mailadmin.sh" >> /root/.bashrc

EXPOSE 1025 2225 2525 25 9000
ENTRYPOINT ["/mnt/common/executable/bash/entrypoint.sh"]
