#!/usr/bin/env bash

addgroup phpbb --gid $GID
adduser --disabled-password --ingroup phpbb --gecos "" --uid $UID phpbb

echo "Starting php-fpm..."
php-fpm --allow-to-run-as-root >/dev/null 2>&1 &
sleep 1

echo "Run PHP"
service php7.0-fpm start
service php7.0-fpm restart
service php7.0-fpm status

echo "Run nginx..."
nginx -g 'daemon off;'