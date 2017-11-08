#!/bin/bash
set -e

trap "exit" INT

#/mnt/common/executable/bash/control-daemon.sh /var/run/syslog-ng.pid /var/spool/postfix/pid/master.pid /usr/sbin/postfix start

# Arguments
pidfile_syslog_ng="$1"
shift
pidfile_postfix="$1"
shift
command=$@

$command
sleep 2
tail -F /var/log/mail.log &
sleep 2
# If file pid exist and process id pid exists
while [ -f $pidfile_syslog_ng ] && [ -f $pidfile_postfix ] && kill -0 $(cat $pidfile_syslog_ng) && kill -0 $(cat $pidfile_postfix); do
    sleep 2
done

exit 1