#!/bin/bash
set -e

sed -i "s/access_log/#access_log/g" /etc/nginx/nginx.conf
sed -i "s/error_log/#error_log/g" /etc/nginx/nginx.conf
echo "daemon off;" >> /etc/nginx/nginx.conf
echo "error_log /dev/stdout info;" >> /etc/nginx/nginx.conf
sed -e ':a' -e 'N' -e '$!ba' -e 's#http {#http {\naccess_log /dev/stdout;#g' \
  /etc/nginx/nginx.conf > /etc/nginx/nginx.conf_tmp
mv /etc/nginx/nginx.conf_tmp /etc/nginx/nginx.conf

echo "
server {
  listen 80;
  server_name $APT_DOMAIN;

  #access_log /var/log/nginx/packages-error.log;
  #error_log /var/log/nginx/packages-error.log;

  location / {
    root /var/packages;
    index index.html;
    autoindex on;
  }

  location ~ /(.*)/conf {
    deny all;
  }

  location ~ /(.*)/db {
    deny all;
  }

  location ~* ^/.*($DENY_EXTENSIONS)\$ {
    deny all;
  }
}
" > /etc/nginx/sites-enabled/default

exit 0