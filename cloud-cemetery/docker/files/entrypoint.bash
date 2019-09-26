#!/bin/bash

echo "[Init Cloud Cementery]"

if [ -z "$DAYS_TO_DROP" ]; then
	DAYS_TO_DROP="32"
fi

for d in $(ls /sa/*); do
	echo "[INFO] Process file $d project $(cat $d | jq .project_id | tr -d '"')"
	gcloud auth activate-service-account --key-file $d
	gcloud config set project $(cat $d | jq .project_id | tr -d '"')
	for s in $(gcloud compute snapshots list | grep -v NAME | awk '{ print $1 }'); do
		describe_snapshot="$(gcloud compute snapshots describe $s)"
		echo -n "."
		if [ "null" != "$(echo "$describe_snapshot" | yq '.labels')" ]; then
			echo ""
			echo "[INFO] Looking pulse: $s"
			if [ "true" == "$(echo "$describe_snapshot" | yq '.labels' | jq '.["funeral-home"]' | tr -d '"' | tr '[:upper:]' '[:lower:]')" ] \
				|| [ "true" == "$(echo "$describe_snapshot" | yq '.labels' | jq '.["cementery"]' | tr -d '"' | tr '[:upper:]' '[:lower:]')" ]; then
				dead_date=$(echo "$describe_snapshot" | yq '.creationTimestamp' | tr -d '"' | cut -d 'T' -f1)
				echo "[INFO] $s dead since day $dead_date"
				if [ $(date +%s) -ge $(date -d "$dead_date+$DAYS_TO_DROP days" +%s) ]; then
					echo $(date +%s)
					echo $(date -d "$dead_date+$DAYS_TO_DROP days" +%s)
					echo "[INFO] Incineration snapshot $s, zone $(echo "$describe_snapshot" | yq '.sourceDisk' | cut -d "/" -f9)"
					# --zone $(echo $(echo "$describe_snapshot" | yq '.sourceDisk' | cut -d "/" -f9))
					echo -ne '\n' | gcloud compute snapshots delete $s
				fi
			fi
		fi
	done
done