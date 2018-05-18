#!/bin/bash
set -e
trap "exit" INT

state=0
while [ $state = 1 ]
do
	for arg in "$@"
	do
		if [ -f $arg ] && kill -0 $(cat $arg)
		then
			state=0
		else
			echo "[ERROR] Error in pid $arg"
			state=1
		fi
	done
    sleep 2
done

exit 1