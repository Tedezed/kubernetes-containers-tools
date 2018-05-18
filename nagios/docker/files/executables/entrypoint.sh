#!/bin/bash

echo "v 0.0.1"

# Start apache2
source /etc/apache2/envvars
/usr/sbin/apache2 -X &

# Start Nagios
/usr/sbin/nagios3 -d /etc/nagios3/nagios.cfg &

# Start control-daemon apache2 nagios3
/files/control-daemon.sh /var/run/apache2/apache2.pid /var/run/nagios3/nagios3.pid