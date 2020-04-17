#!/bin/bash
set -e

echo "[INFO] Start Nginx"
nginx -c /etc/nginx/nginx.conf 

exit 0