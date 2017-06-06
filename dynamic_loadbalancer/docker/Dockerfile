FROM debian:jessie-backports
MAINTAINER Juan Manuel Torres (Tedezed) <juanmanuel.torres@aventurabinaria.es>

ENV KMASTER kubernetes
ENV ADD_HOST "127.0.0.1 localhost"
ENV NAMESPACE default
ENV TIME_QUERY 17
ENV CONF_KUBE_BASE64 add
ENV NAME_SET "nginx"
ENV TYPE_BALANCE "roundrobin"
ENV COOKIE "false"
ENV TYPE_SET "statefulset"

##### PYTHON

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
    && rm -rf /var/lib/apt/lists/*

RUN pip install pykube deepdiff
ADD slug_dynamic_loadbalancer/ /slug_dynamic_loadbalancer

##### HAPROXY

RUN echo deb http://httpredir.debian.org/debian jessie-backports main | \
      sed 's/\(.*\)-sloppy \(.*\)/&@\1 \2/' | tr @ '\n' | \
      tee /etc/apt/sources.list.d/backports.list

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get autoremove -y \
    && apt-get install -y \
    	haproxy -t jessie-backports \
    && rm -rf /var/lib/apt/lists/*

#### END

ADD files/docker-entrypoint.sh /usr/local/bin/
RUN chmod +rx /usr/local/bin/docker-entrypoint.sh

USER root
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["/bin/bash"]
