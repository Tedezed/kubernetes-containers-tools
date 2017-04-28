FROM debian:jessie
MAINTAINER Juan Manuel Torres (Tedezed) <juanmanuel.torres@aventurabinaria.es>

ENV KMASTER kubernetes
ENV ADD_HOST "127.0.0.1 localhost"
ENV NAMESPACE default
ENV HEAPSTER url_heapster
ENV AUTOSCALER_COUNT 10
ENV TIME_QUERY 17
ENV CONF_KUBE_BASE64 add

RUN apt-get update \
    && apt-get install -y \
        python2.7 \
        python-pip \
        git \
        nano \
    && rm -rf /var/lib/apt/lists/*

RUN pip install pykube
RUN git clone https://github.com/Tedezed/slug-containers.git

ADD files/docker-entrypoint.sh /usr/local/bin/
RUN chmod +rx /usr/local/bin/docker-entrypoint.sh
#RUN chmod 777 /usr/local/bin/docker-entrypoint.sh

USER root
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["/bin/bash"]