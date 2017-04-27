FROM debian:jessie
MAINTAINER Juan Manuel Torres (Tedezed) <juanmanuel.torres@aventurabinaria.es>

ENV KMASTER kubernetes
ENV NAMESPACE default
ENV HEAPSTER url_heapster
ENV AUTOSCALER_COUNT 10
ENV TIME_QUERY 17
ENV CONF_KUBE add

RUN apt-get update \
    && apt-get install -y \
        python2.7 \
        python-pip \
        git \
    && rm -rf /var/lib/apt/lists/*

RUN pip install pykube
RUN git clone https://github.com/Tedezed/slug-containers.git

COPY files/docker-entrypoint.sh /usr/local/bin/

ENTRYPOINT ["docker-entrypoint.sh"]