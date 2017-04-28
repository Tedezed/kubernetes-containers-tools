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

from tools import *

# RUN!
os.system('echo "Start Slug StatefulSet Autoscaler v.0.0.1"')
# python main.py namespace="default" url_heapster="http://heapster/api/v1/model" autoscaler_count="5" time_query="10"
patch_exec = os.path.dirname(os.path.realpath(__file__)) + "/"
api = pykube.HTTPClient(pykube.KubeConfig.from_file(patch_exec + "credentials/config"))

#Arguments
list_argv=[]
sys.argv.remove(sys.argv[0])
for elements in sys.argv:
	variable_entrada = elements.split("=")
	if len(variable_entrada) == 1 or variable_entrada[1] == '':
		raise NameError('[ERROR] Invalid Arguments [python example.py var="text"]')
	list_argv.append(variable_entrada)

dic_argv = argument_to_dic(list_argv)
namespace = dic_argv["namespace"]
url_heapster = dic_argv["url_heapster"]
autoscaler_count = dic_argv["autoscaler_count"]
time_query = int(dic_argv["time_query"])

if int(autoscaler_count) < 3:
	autoscaler_count = "3"
if time_query < 5:
	time_query = "5"

while True:
	list_set = select_statefulset(api, namespace)
	list_set = select_pod_form_set(api, list_set, namespace, url_heapster)
	list_set = percent_cpu_set(list_set)

	pre_set = pykube.StatefulSet.objects(api).filter(namespace=namespace)
	change = 0
	set_scaling = 0
	for sfs in pre_set:
		for setfull in list_set:
			os.system('echo "[StatefulSet] %s %s CPU - Autoscale in %s CPU reduce in %s CPU"' % (sfs.name, setfull["percent_cpu"], setfull["autoscaler_percent_cpu"],setfull["autoreduce_percent_cpu"]))
			replicas = int(sfs.obj["spec"]["replicas"])
			if sfs.obj["metadata"]["labels"]["autoscaler_count"] == "0":
				# Autoscale
				if sfs.obj["metadata"]["name"] == setfull["name"] and int(setfull["autoscaler_percent_cpu"]) <= int(setfull["percent_cpu"]):
					sfs.obj["spec"]["replicas"] = replicas + 1
					sfs.obj["metadata"]["labels"]["autoscaler_count"] = autoscaler_count
					set_scaling += 1
				# Autoreduce Normal
				elif sfs.obj["metadata"]["name"] == setfull["name"] and int(setfull["autoreduce_percent_cpu"]) >= int(setfull["percent_cpu"]) and setfull["autoreduce_normal"].lower() == "true":
					sfs.obj["spec"]["replicas"] = replicas - 1
					sfs.obj["metadata"]["labels"]["autoscaler_count"] = autoscaler_count
					set_scaling += 1
				if set_scaling != 0:
					if int(setfull["min_replicas"]) <= sfs.obj["spec"]["replicas"] and int(setfull["max_replicas"]) >= sfs.obj["spec"]["replicas"]:
						pykube.StatefulSet(api, sfs.obj).update()
						os.system('echo "[AUTOSCALING] %s replicas: min %s max %s "' % (sfs.obj["metadata"]["name"], setfull["min_replicas"], setfull["max_replicas"]))
						os.system('echo "[AUTOSCALING] %s replicas: %s to %s "' % (sfs.obj["metadata"]["name"], replicas, sfs.obj["spec"]["replicas"]))
						change += 1
			else:
				# Reduce only autoscaler_count
				sfs.obj["metadata"]["labels"]["autoscaler_count"] = str(int(sfs.obj["metadata"]["labels"]["autoscaler_count"]) - 1)
				os.system('echo "[INFO] Seelp StatefulSet %s replicas %s, attempts %s"' % (sfs.obj["metadata"]["name"], sfs.obj["spec"]["replicas"], sfs.obj["metadata"]["labels"]["autoscaler_count"]))
				pykube.StatefulSet(api, sfs.obj).update()

	os.system('echo "[INFO] StatefulSet autoscaler %s"' % (change))
	os.system('echo "Seelp %ss for next query"' % (time_query))
	time.sleep(time_query)