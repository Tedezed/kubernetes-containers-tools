FROM httpd:latest
MAINTAINER Juan Manuel Torres <juanmanuel.torres@aventurabinaria.es>

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
	&& apt-get install -y nagios3 nagios-nrpe-server nagios-nrpe-plugin nagios-plugins

RUN apt-get install -y wget nano unzip apache2-utils \
 && a2enmod rewrite \
 && a2enmod cgi

ENV NAGIOS_PASS="nagiospass"

ADD files /files
RUN chmod +x /files/executables/*

EXPOSE 80 443
ENTRYPOINT ["/files/executables/entrypoint.sh"]