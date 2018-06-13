FROM httpd:latest
MAINTAINER Juan Manuel Torres <juanmanuel.torres@aventurabinaria.es>

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
	&& apt-get install -y nagios3 nagios-nrpe-server nagios-nrpe-plugin nagios-plugins

RUN apt-get update \
	&& apt-get install -y wget nano git unzip apache2-utils mysql-client \
		libmysqlclient-dev libdbd-mysql-perl build-essential make automake \
 	&& a2enmod rewrite \
 	&& a2enmod cgi

ENV NAGIOS_DIR="/usr/local/nagios" \
	NAGIOS_USER="nagios" \
	NAGIOS_PASS="nagios" \
	NAGIOS_DEBUG="OFF" \
	MYSQL_USER="nagios" \
	MYSQL_PASSWORD="nagios" \
	MYSQL_HOST="mysql" \
	MYSQL_DATABASE="nagios"

RUN cd /tmp \
    && wget -O ndoutils.tar.gz https://github.com/NagiosEnterprises/ndoutils/archive/ndoutils-2.1.3.tar.gz \
    && tar xzf ndoutils.tar.gz \
    && cd /tmp/ndoutils-ndoutils-2.1.3/ \
    && ./configure \
        --prefix="${NAGIOS_DIR}" \
        --enable-mysql \
    && make all \
	&& make install

ADD files /files
RUN chmod +x /files/executables/* \
	&& mkdir -p /etc/nagios3/custom

EXPOSE 80 443
VOLUME ["/etc/nagios3/custom"]
ENTRYPOINT ["/files/executables/entrypoint.sh"]