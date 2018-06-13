#!/bin/bash
set -e

echo "Start Control Daemon"
echo "$@"

trap "exit" INT

state=0
sleep 10
echo "$(ps -aux)"
while [ $state = 0 ]
do
	for arg in "$@"
	do
		#echo "$(cat $arg)"
		if [ -f $arg ] && kill -0 $(cat $arg)
		then
			state=0
		else
			echo "[ERROR] Error in file pid $arg"
			if [ $NAGIOS_DEBUG == "ON" ]; then
				sleep 10
			else
				state=1
				break
			fi
		fi
	done
    sleep 2
done

exit 1