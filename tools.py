#!/usr/bin/python

# Copyright 2017 Tedezed
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# By: https://github.com/Tedezed
# juanmanuel.torres@aventurabinaria.es

import time
import requests
import pykube
import json
import os
import sys

def avg_list(list):
	return sum(list)/len(list)

def argument_to_dic(list):
	dic = {}
	for z in list:
		dic[z[0]]=z[1]
	return dic

def select_statefulset(api, namespace):
	pre_set = pykube.StatefulSet.objects(api).filter(namespace=namespace)
	list_set = []
	for s in pre_set.response['items']:
		try:
			dic_set = {}
			dic_set["name"] = s["metadata"]["name"]
			dic_set["autoscaler"] = s["metadata"]["labels"]["autoscaler"].lower()
			dic_set["autoscaler_percent_cpu"] = s["metadata"]["labels"]["autoscaler_percent_cpu"]
			dic_set["autoscaler_count"] = s["metadata"]["labels"]["autoscaler_count"]
			dic_set["limit_cpu"] = s["spec"]["template"]["spec"]["containers"][0]["resources"]["limits"]["cpu"][0:-1]
			if dic_set["autoscaler"] == "true":
				list_set.append(dic_set)
		except:
			print "[ERROR] Error to add %s" % (s["metadata"]["name"])
	return list_set

def select_pod_form_set(api, list_set, namespace, url_heapster):
	pre_pod = pykube.Pod.objects(api).filter(namespace=namespace)
	#pod_obj = pykube.Pod(api, pre_pod.response['items'][0])
	list_pods = []
	for p in pre_pod.response['items']:
		pod_obj = pykube.Pod(api, p)
		pod_name = pod_obj.name
		set_name = 	json.loads(p["metadata"]["annotations"]["kubernetes.io/created-by"])["reference"]["name"]
		
		re = requests.request('GET', "%s/namespaces/%s/pods/%s/metrics/cpu/usage_rate" % (url_heapster, namespace, pod_name))
		
		#lit_usage_cpu = []
		#for i in re.json()["metrics"]:
		#	lit_usage_cpu.append(i["value"])
		#avg_cpu = avg_list(lit_usage_cpu)

		# Latest cpu usage
		for i in re.json()["metrics"]:
			if i["timestamp"] == re.json()["latestTimestamp"]:
				avg_cpu = i["value"]

		num = 0
		dic_pod = {}
		for e in list_set:
			if e["name"] == set_name:
				dic_pod["name"] = pod_name
				dic_pod["set_name"] = set_name
				dic_pod["avg_cpu"] = avg_cpu
				list_pods.append(dic_pod)
				list_set[num]["list_pods"] = list_pods
			num +=1
	return list_set

def percent_cpu_set(list_set):
	num = 0
	for setfull in list_set:
		if setfull["autoscaler"] == "true":
			list_cpu = []
			for z in setfull["list_pods"]:
				list_cpu.append(z["avg_cpu"])

			limit_cpu = float(setfull["limit_cpu"])
			avg_cpu_pod = float(avg_list(list_cpu))

			percent_cpu = int(avg_cpu_pod/limit_cpu*100)
			list_set[num]["percent_cpu"] = percent_cpu
		num +=1
	return list_set
