FROM debian:jessie
MAINTAINER Juan Manuel Torres <juanmanuel.torres@aventurabinaria.es>

ENV DEBIAN_FRONTEND="noninteractive" \
	RELAYHOST="in.mailjet.com" \
	RELAYHOST_PORT="2525" \
	SMTP_KEY="XXX" \
	SMTP_SECRET="xxx" \
	NETWORKS="0.0.0.0/0" \
	DNS="8.8.4.4"

ADD common/executable/bash/init.sh /init.sh
RUN chmod +x /init.sh \
	&& bash /init.sh

RUN apt-get update && apt-get -y install postfix libsasl2-2 libsasl2-modules syslog-ng locales dbus tcpdump nano
RUN export LANG=C \
    && locale-gen es_ES.UTF-8 \
    && update-locale \
    && export LANG=es_ES.UTF-8 \
    && export LC_CTYPE=es_ES.UTF-8 \
    && export LC_ALL=es_ES.UTF-8
RUN rm -rf /var/lib/apt/lists/*

RUN sed -i -E 's/^(\s*)system\(\);/\1unix-stream("\/dev\/log");/' /etc/syslog-ng/syslog-ng.conf \
	&& sed -i 's/^#\(SYSLOGNG_OPTS="--no-caps"\)/\1/g' /etc/default/syslog-ng

ADD common/ /mnt/common
RUN chmod +x /mnt/common/executable/bash/entrypoint.sh \
	&& chmod +x /mnt/common/executable/bash/control-daemon.sh

EXPOSE 25
ENTRYPOINT ["/mnt/common/executable/bash/entrypoint.sh"]