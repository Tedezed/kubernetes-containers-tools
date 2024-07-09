#!/bin/bash
set -xe

echo "version: 0.1"

mkdir -p /var/packages/${APT_REPOSITORY}/conf
mkdir -p /usr/src/pagespeed/
mkdir -p /root/.gnupg

chmod 777 -R /root/.gnupg
chown root:root -R /root/.gnupg

exit 0

