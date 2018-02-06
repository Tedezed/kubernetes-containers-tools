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
        wget \
        gcc \
    && rm -rf /var/lib/apt/lists/*

# Personal Nginx

RUN apt-get remove nginx -y \
    && rm -rf /usr/local/nginx /usr/sbin/nginx /etc/nginx /usr/local/nginx/ /usr/local/nginx/

RUN apt-get update \
    && apt-get install build-essential g++ libpcre3 libpcre3-dev libssl-dev zlibc zlib1g zlib1g-dev checkinstall libgeoip-dev -y \
    && rm -rf /var/lib/apt/lists/*

RUN cd /usr/src/ \
    && curl -O http://nginx.org/download/nginx-1.10.3.tar.gz \
    && ls \
    && tar -xzf nginx-1.10.3.tar.gz

RUN cd /usr/src/nginx-1.10.3 \
    && curl -O https://bitbucket.org/nginx-goodies/nginx-sticky-module-ng/get/1.2.6.tar.gz \
    && tar -xzf 1.2.6.tar.gz

RUN mkdir /var/cache/nginx \
    && chown www-data /var/cache/nginx \
    && mkdir /var/cache/nginx/client_temp \
    /var/cache/nginx/proxy_temp \
    /var/cache/nginx/fastcgi_temp \
    /var/cache/nginx/uwsgi_temp \
    /var/cache/nginx/scgi_temp \
    && cd /usr/src/nginx-1.10.3 \
    && ls \
    && ./configure --prefix=/etc/nginx \
    --sbin-path=/usr/sbin/nginx \
    --conf-path=/etc/nginx/nginx.conf \
    --error-log-path=/var/log/nginx/error.log \
    --http-log-path=/var/log/nginx/access.log \
    --pid-path=/var/run/nginx.pid \
    --lock-path=/var/run/nginx.lock \
    --http-client-body-temp-path=/var/cache/nginx/client_temp \
    --http-proxy-temp-path=/var/cache/nginx/proxy_temp \
    --http-fastcgi-temp-path=/var/cache/nginx/fastcgi_temp \
    --http-uwsgi-temp-path=/var/cache/nginx/uwsgi_temp \
    --http-scgi-temp-path=/var/cache/nginx/scgi_temp \
    --user=www-data \
    --group=www-data \
    --with-http_ssl_module \
    --with-http_realip_module \
    --with-http_addition_module \
    --with-http_sub_module \
    --with-http_dav_module \
    --with-http_flv_module \
    --with-http_mp4_module \
    --with-http_gunzip_module \
    --with-http_gzip_static_module \
    --with-http_random_index_module \
    --with-http_secure_link_module \
    --with-http_stub_status_module \
    --with-mail \
    --with-mail_ssl_module \
    --with-file-aio \
    --with-cc-opt='-g -O2 -fstack-protector --param=ssp-buffer-size=4 -Wformat -Werror=format-security -Wp,-D_FORTIFY_SOURCE=2' \
    --with-ld-opt='-Wl,-z,relro -Wl,--as-needed' \
    --with-ipv6 \
    --with-http_geoip_module \
    --add-module=nginx-goodies-nginx-sticky-module-ng-c78b7dd79d0d

RUN cd /usr/src/nginx-1.10.3 \
    && ls \
    && make
RUN cd /usr/src/nginx-1.10.3 \
    && make install \
    && chmod a+x /etc/init.d/nginx \
    && rm -rf /usr/src/*

RUN mkdir /etc/nginx/geoip \
    && cd /etc/nginx/geoip \
    && wget http://geolite.maxmind.com/download/geoip/database/GeoLiteCountry/GeoIP.dat.gz \
    && gunzip GeoIP.dat.gz \
    && wget http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz \
    && gunzip GeoLiteCity.dat.gz \
    && chown www-data -R /etc/nginx/geoip

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

ENV NAME_LIBERTY="liberty" TIMEOUT="60m"

EXPOSE 80
EXPOSE 443
VOLUME ["/etc/nginx/sites-enabled", "/etc/nginx/certs", "/etc/nginx/conf.d", "/var/log/nginx", "/var/www/html"]
USER root
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["/bin/bash"]