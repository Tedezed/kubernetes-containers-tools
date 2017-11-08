FROM debian:jessie
MAINTAINER Juan Manuel Torres <juanmanuel.torres@aventurabinaria.es>

ENV DEBIAN_FRONTEND="noninteractive" \
	RELAYHOST="in.mailjet.com" \
	RELAYHOST_PORT="2525" \
	SMTP_KEY="XXX" \
	SMTP_SECRET="xxx"\
	HOSTNAME="mailjet"

RUN apt-get update && apt-get -y install postfix libsasl2-modules syslog-ng

RUN sed -i -E 's/^(\s*)system\(\);/\1unix-stream("\/dev\/log");/' /etc/syslog-ng/syslog-ng.conf \
	&& sed -i 's/^#\(SYSLOGNG_OPTS="--no-caps"\)/\1/g' /etc/default/syslog-ng

ADD common/ /mnt/common
RUN chmod +x /mnt/common/executable/bash/entrypoint.sh \
	&& chmod +x /mnt/common/executable/bash/control-daemon.sh

EXPOSE 25
ENTRYPOINT ["/mnt/common/executable/bash/entrypoint.sh"]