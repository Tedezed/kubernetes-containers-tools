#!/bin/bash
set -e

echo "Start Control Daemon"
echo "$(ps -aux)"
echo "$@"

trap "exit" INT

state=0
while [ $state = 0 ]
do
	for arg in "$@"
	do
		echo "$(cat $arg)"
		if [ -f $arg ] && kill -0 $(cat $arg)
		then
			state=0
		else
			echo "[ERROR] Error in file pid $arg"
			state=1
			break
		fi
	done
    sleep 2
done

exit 1