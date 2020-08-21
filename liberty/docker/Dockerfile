#FROM nginx:latest
FROM debian:buster-slim

# Ingress Controller Liberty
# Creator: Juan Manuel Torres
# Source: https://github.com/Tedezed
# Mail: juanmanuel.torres@aventurabinaria.es

MAINTAINER Juan Manuel Torres <juanmanuel.torres@aventurabinaria.es>

ENV KMASTER="kubernetes" \
    TIME_QUERY="17"\
    TYPE_BALANCE="roundrobin"\
    COOKIE="false"

WORKDIR /etc/nginx

COPY preferences /etc/apt/preferences
RUN echo "deb http://ftp.us.debian.org/debian stable main contrib non-free" >> /etc/apt/sources.list \
    && echo "deb http://ftp.us.debian.org/debian unstable main contrib non-free" >> /etc/apt/sources.list \
    && apt-get update \
    && apt-get install -t stable -y \
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
        cmake \
        make \
        pkg-config \
        libjansson-dev \
        bison \
        libexpat1-dev \
        expect \
        libgd-dev \
        gettext \
        libjansson-dev \
        libjpeg-dev \
        libc6-dev \
        libc-dev-bin \
        linux-headers-amd64 \
        libopenjp2-7-dev \
        libldap2-dev \
        libghc-regex-pcre-dev \
        libperl-dev \
        libreadline-dev \
        libsqlite0-dev \
        libghc-zlib-dev \
        build-essential \
        libpcre3 \
        libpcre3-dev \
        libssl-dev \
        zlibc \
        zlib1g \
        zlib1g-dev \
        libgeoip-dev \
        libctpp2-2v5 \
        ctpp2-utils \
        libctpp2-dev \
        libgd-dev \
    && apt-get install -t unstable -y gcc-9 g++-9 libint-dev
##    && rm -rf /var/lib/apt/lists/*
##    && echo "deb http://ftp.us.debian.org/debian unstable main contrib non-free" >> /etc/apt/sources.list \
##    && apt-get update \
##    && apt-get -t unstable install libintl-perl -y \
##        postgresql-dev zlib-dev

# # Old apt: checkinstall
# RUN apt-get update \
#     && apt-get install build-essential libpcre3 libpcre3-dev libssl-dev zlibc zlib1g zlib1g-dev libgeoip-dev -y \
#     && rm -rf /var/lib/apt/lists/*

# RUN cd /usr/src/ \
#     && curl -O http://nginx.org/download/nginx-1.17.10.tar.gz \
#     && ls \
#     && tar -xzf nginx-1.17.10.tar.gz && mv nginx-1.17.10 nginx
#
#     && ./configure 

RUN cd /usr/src/ \
    &&  git clone --recursive https://github.com/Code-Mirror/nginx.git

# RUN cd /usr/src/nginx-1.17.10 \
#     && curl -O https://bitbucket.org/nginx-goodies/nginx-sticky-module-ng/get/1.2.6.tar.gz \
#     && tar -xzf 1.2.6.tar.gz
# #    && git clone https://github.com/Tedezed/nginx_upstream_check_module

# New modules from RekGRpth
RUN mkdir -p /usr/src \
    && cd /usr/src \
    && git clone --recursive https://github.com/Code-Mirror/ctpp2.git \
    && git clone --recursive https://github.com/Code-Mirror/libjwt.git \
    && mkdir -p /usr/src/nginx/modules \
    && cd /usr/src/nginx/modules \
    && git clone --recursive https://github.com/Code-Mirror/set-misc-nginx-module.git \
    && git clone --recursive https://github.com/Code-Mirror/form-input-nginx-module.git \
    && git clone --recursive https://github.com/Code-Mirror/encrypted-session-nginx-module.git \
    && git clone --recursive https://github.com/Code-Mirror/echo-nginx-module.git \
    && git clone --recursive https://github.com/Code-Mirror/ngx_ctpp2.git \
    && git clone --recursive https://github.com/Code-Mirror/ngx_http_captcha_module.git \
    && git clone --recursive https://github.com/Code-Mirror/headers-more-nginx-module.git \
    && git clone --recursive https://github.com/Code-Mirror/nginx-sticky-module-ng.git

RUN mkdir -p /etc/nginx/ /var/lib/nginx \
    && touch /etc/init.d/nginx \
    && mkdir -p /var/www/error \
    && chown -R www-data:www-data /etc/nginx \
    && chown -R www-data:www-data /var/lib/nginx \
    && chown -R www-data:www-data /var/www

RUN cd /usr/src/libjwt \
    && cmake . -DBUILD_SHARED_LIBS=true && make -j"$(nproc)" install

COPY NimbusSans-Regular.ttf /usr/local/share/fonts/
# echo "deb http://ftp.us.debian.org/debian testing main contrib non-free" >> /etc/apt/sources.list

# ctpp2
# Path for libs:
#   /lib
#   /opt/lib
#   /usr/lib
#   /usr/local/lib
# RUN apt-get install -y \
#         libctpp2-2v5 \
#         ctpp2-utils \
#         libctpp2-dev \
#         libgd-dev
        # gettext \
        # gettext-base \
        # libgettextpo-dev \
        # libgettextpo0

#RUN curl https://pkg.freebsd.org/FreeBSD:13:amd64/latest/All/gettext-runtime-0.20.1.txz -o /gettext-runtime-0.20.1.txz && tar -xf gettext-runtime-0.20.1.txz
#RUN sleep 999999 && cd /usr/src/ctpp2 \
#    && cmake . -DCMAKE_INSTALL_PREFIX=/usr/local && make -j"$(nproc)" install

#   Nginx
RUN mkdir /var/cache/nginx \
    && chown www-data /var/cache/nginx \
    && mkdir /var/cache/nginx/client_temp \
    /var/cache/nginx/proxy_temp \
    /var/cache/nginx/fastcgi_temp \
    /var/cache/nginx/uwsgi_temp \
    /var/cache/nginx/scgi_temp \
    && ls /usr/src/ \
    && cd /usr/src/nginx \
    && auto/configure \
    --prefix=/etc/nginx \
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
    --with-http_auth_request_module \
    --with-http_image_filter_module=dynamic \
    --with-pcre \
    --with-pcre-jit \
    --with-stream=dynamic \
    --with-stream_realip_module \
    --with-stream_ssl_module \
    --with-stream_ssl_preread_module \
    --with-threads \
    --with-mail \
    --with-mail_ssl_module \
    --with-file-aio \
    --with-cc-opt='-g -O2 -fstack-protector --param=ssp-buffer-size=4 -Wformat -Werror=format-security -Wp,-D_FORTIFY_SOURCE=2' \
    --with-ld-opt='-Wl,-z,relro -Wl,--as-needed' \
    --with-ipv6 \
    --with-http_geoip_module \
    --with-http_v2_module \
    --add-dynamic-module="$(find modules -type f -name "config" | grep -v "\.git" | grep -v "\/t\/" | while read -r NAME; do echo -n "$(dirname "$NAME") "; done)"

RUN cd /usr/src/nginx \
    && ls \
    && make \
    && cd /usr/src/nginx \
    && make install \
    && chmod a+x /etc/init.d/nginx \
    && rm -rf /usr/src/*

# http://geolite.maxmind.com/download/geoip/database/GeoLiteCountry/GeoIP.dat.gz
# http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz
# RUN mkdir /etc/nginx/geoip \
#     && cd /etc/nginx/geoip \
#     && wget https://geolite.maxmind.com/download/geoip/database/GeoLite2-Country.tar.gz \
#     && gunzip GeoLite2-Country.tar.gz \
#     && wget https://geolite.maxmind.com/download/geoip/database/GeoLite2-City.tar.gz \
#     && gunzip GeoLite2-City.tar.gz \
#     && chown www-data -R /etc/nginx/geoip

RUN pip install kubernetes deepdiff elasticsearch \
    && rm -rf /etc/nginx/conf.d/default.conf \
    && ls /etc/nginx/ -lia \
    && apt-get update \
    && apt-get install -y apache2-utils \
    && rm -rf /var/lib/apt/lists/*

ENV NAME_LIBERTY="liberty" \
    DEFAULT_CERT="false" \
    DEFAULT_CERT_NAMESPACE="false" \
    TIMEOUT="60m" \
    MODE="production" \
    ELK="false" \
    ELK_MODE="stop" \
    ELK_LIBERTY_NAMES="liberty1 liberty2" \
    ELK_HOST="localhost" \
    ELK_PORT="9200" \
    ELK_PREFIX="filebeat" \
    ELK_DAYS=3 \
    SECRET_USER="admin" \
    SECRET_PASSWD="admin1234567890" \
    SUPPORT_EMAIL="soporte@guadaltech.es" \
    TEAM_NAME="Support Team" \
    NAMESPACE_CERT_GENERATOR="default" \
    SVC_CERT_GENERATOR="kube-lego-nginx" \
    SVC_CERT_GENERATOR_PORT="8080" \
    IP_ERROR="127.0.0.1" \
    PORT_ERROR="3502" \
    CUSTOM_CAPTCHA_SECRET="secret"

ARG NUMBITS=2048

ADD files/ /files
RUN mkdir -p /files/liberty-ingress/default-cert/ \
  && mkdir -p /files/liberty-ingress/certs/ \
  && openssl dhparam -out /files/liberty-ingress/dhparam.pem $NUMBITS
RUN mkdir -p /etc/nginx/html/static/ \
  && cp -R /files/static/* /etc/nginx/html/static/ && rm -rf /files/static \
  && mkdir -p /etc/nginx/html/login/ \
  && cd /files/login && ctpp2c login.html login.html.ct2 \
  && cp -R /files/login/login.html.ct2 /etc/nginx/html/login/login.html.ct2 \
  && cp -R /files/error/ /var/www/error \
  && cp /files/docker-entrypoint.sh /usr/local/bin/ \
  && chmod +rx /usr/local/bin/docker-entrypoint.sh \
  && mkdir /etc/nginx/others \
  && cp /files/nginx.conf /etc/nginx/nginx.conf \
  && chown www-data:www-data -R /etc/nginx/others \
  && chown www-data:www-data -R /files/error \
  && chown www-data:www-data -R /files/liberty-ingress/default-cert

#RUN sleep 99999

EXPOSE 80
EXPOSE 443
VOLUME ["/etc/nginx/sites-enabled", "/etc/nginx/certs", "/etc/nginx/conf.d", "/var/log/nginx", "/var/www/html"]
USER root
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["/bin/bash"]