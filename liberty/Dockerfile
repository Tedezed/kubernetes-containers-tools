#FROM nginx:latest
FROM debian:stretch-slim

ENV KMASTER="kubernetes" \
    TIME_QUERY="17"\
    TYPE_BALANCE="roundrobin"\
    COOKIE="false"

WORKDIR /etc/nginx

# Install Nginx.
RUN \
  apt-get update && \
  apt-get install -y nginx && \
  rm -rf /var/lib/apt/lists/* && \
  echo "\ndaemon off;" >> /etc/nginx/nginx.conf && \
  chown -R www-data:www-data /var/lib/nginx

RUN apt-get update \
    && apt-get install -y \
    	curl \
    	rsyslog \
    	apt-transport-https \
        python2.7 \
        python-pip \
        python-jinja2 \
        git \
        nano \
        procps \
    && rm -rf /var/lib/apt/lists/*

RUN pip install kubernetes deepdiff

RUN rm -rf /etc/nginx/conf.d/default.conf

RUN ls /etc/nginx/ -lia

ADD files/ /files
RUN cp -R /files/error/ /var/www/error \
  && cp /files/docker-entrypoint.sh /usr/local/bin/ \
  && chmod +rx /usr/local/bin/docker-entrypoint.sh \
  && mkdir /etc/nginx/others \
  && cp /files/nginx.conf /etc/nginx/nginx.conf \
  && chown www-data:www-data -R /etc/nginx/others \
  && chown www-data:www-data -R /files/error \
  && chown www-data:www-data -R /files/liberty-ingress/default-cert

EXPOSE 80
EXPOSE 443
VOLUME ["/etc/nginx/sites-enabled", "/etc/nginx/certs", "/etc/nginx/conf.d", "/var/log/nginx", "/var/www/html"]
USER root
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["/bin/bash"]