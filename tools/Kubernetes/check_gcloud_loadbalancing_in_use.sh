#!/bin/bash

pool_list=$(gcloud compute target-pools list | grep -v NAME |awk '{ print $1":"$2 }')
svc_list=$(kubectl get svc --all-namespaces | grep LoadBalancer | grep -v NAME |awk '{ print $1"/"$2 }')

for pool in ${pool_list[@]}
do
	array=(${pool//:/ }) # split
	load_balancing_of_x=$(gcloud compute target-pools describe ${array[0]} --region=${array[1]} | grep description | grep -o '"[a-zA-Z\-]*/[a-zA-Z\-]*"')
	for svc in ${svc_list[@]}
	do
		if [ $load_balancing_of_x -ne "\"$svc\"" ]; then
			echo $svc
		fi
	done
done