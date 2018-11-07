#!/usr/bin/python
# -*- coding: utf-8 -*-

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

import time, requests, pykube, json, os, sys

def avg_list(list):
	return sum(list)/len(list)

def argument_to_dic(list):
	dic = {}
	for z in list:
		dic[z[0]]=z[1]
	return dic

def select_statefulset(api, namespace):
	pre_set = pykube.StatefulSet.objects(api)
	list_set = []
	try:
		for s in pre_set.response['items']:
			if str(s["metadata"]["namespace"]) == str(namespace):
				try:
					dic_set = {}
					dic_set["name"] = s["metadata"]["name"]
					dic_set["slug-autoscaler/autoscaler"] = s["spec"]["template"]["metadata"]["annotations"]["slug-autoscaler/autoscaler"].lower()
					dic_set["autoscaler_percent_cpu"] = s["spec"]["template"]["metadata"]["annotations"].get("slug-autoscaler/autoscaler_percent_cpu", "50")
					dic_set["autoreduce_normal"] = s["spec"]["template"]["metadata"]["annotations"].get("slug-autoscaler/autoreduce_normal", "true").lower()
					dic_set["autoreduce_percent_cpu"] = s["spec"]["template"]["metadata"]["annotations"].get("slug-autoscaler/autoreduce_percent_cpu", "10")
					dic_set["autoscaler_count"] = s["spec"]["template"]["metadata"]["annotations"].get("slug-autoscaler/autoscaler_count", "2")
					dic_set["min_replicas"] = s["spec"]["template"]["metadata"]["annotations"].get("slug-autoscaler/min_replicas", "1")
					dic_set["max_replicas"] = s["spec"]["template"]["metadata"]["annotations"].get("slug-autoscaler/max_replicas", "2")
					dic_set["limit_cpu"] = s["spec"]["template"]["spec"]["containers"][0]["resources"]["limits"]["cpu"][0:-1]
					if dic_set["slug-autoscaler/autoscaler"] == "true":
						list_set.append(dic_set)
				except Exception as e:
					print "[ERROR] Error to add %s" % (s["metadata"]["name"])
					print "Exception: %s" % e
	except AttributeError as e:
		print "AttributeError: %s" % e
	return list_set

def select_pod_form_set(api, list_set, namespace, url_heapster):
	pre_pod = pykube.Pod.objects(api)
	list_pods = []
	avg_cpu = 0
	try:
		for p in pre_pod.response['items']:
			if str(p["metadata"]["namespace"]) == str(namespace):
				pod_obj = pykube.Pod(api, p)
				pod_name = pod_obj.name
				
				try:
					set_name = p["metadata"]["annotations"]["slug-autoscaler/sts_owner_name"]
				except Exception as e:
					print "Exception: %s" % e

				try:
					re = requests.request('GET', "%s/namespaces/%s/pods/%s/metrics/cpu/usage_rate" \
					  % (url_heapster, namespace, pod_name))

					# Latest cpu usage
					for i in re.json()["metrics"]:
						if i["timestamp"] == re.json()["latestTimestamp"]:
							avg_cpu = i["value"]
				except Exception as e:
					print "Exception: %s" % e

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
	except AttributeError as e:
		pass
	return list_set

def percent_cpu_set(list_set):
	num = 0
	for setfull in list_set:
		if setfull["slug-autoscaler/autoscaler"] == "true":
			list_cpu = []
			for z in setfull.get("list_pods", {}):
				list_cpu.append(z["avg_cpu"])

			if setfull.get("list_pods", {}) != {}:
				limit_cpu = float(setfull["limit_cpu"])
				avg_cpu_pod = float(avg_list(list_cpu))

				percent_cpu = int(avg_cpu_pod/limit_cpu*100)
				list_set[num]["percent_cpu"] = percent_cpu
			else:
				list_set[num]["percent_cpu"] = 0
		num +=1
	return list_set
