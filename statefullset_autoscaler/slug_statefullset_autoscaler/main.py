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
os.system('echo "Start Slug StatefullSet Autoscaler"')
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

if int(autoscaler_count) < 5:
	autoscaler_count = "5"
if time_query < 10:
	time_query = "10"

while True:
	list_set = select_statefulset(api, namespace)
	list_set = select_pod_form_set(api, list_set, namespace, url_heapster)
	list_set = percent_cpu_set(list_set)

	pre_set = pykube.StatefulSet.objects(api).filter(namespace=namespace)
	set_scaling = 0
	for sfs in pre_set:
		for setfull in list_set:
			os.system('echo "[StatefulSet] %s %s CPU - Autoscale in %s CPU"' % (sfs.name, setfull["percent_cpu"], setfull["autoscaler_percent_cpu"]))
			if sfs.obj["metadata"]["name"] == setfull["name"] and int(setfull["autoscaler_percent_cpu"]) <= int(setfull["percent_cpu"]):
				if sfs.obj["metadata"]["labels"]["autoscaler_count"] == "0":
					sfs.obj["spec"]["replicas"] = int(sfs.obj["spec"]["replicas"]) + 1
					sfs.obj["metadata"]["labels"]["autoscaler_count"] = autoscaler_count
					pykube.StatefulSet(api, sfs.obj).update()
					set_scaling += 1
					os.system('echo "[AUTOSCALING] Scaling StatefulSet %s to %s replicas"' % (sfs.obj["metadata"]["name"], sfs.obj["spec"]["replicas"]))
				else:
					sfs.obj["metadata"]["labels"]["autoscaler_count"] = str(int(sfs.obj["metadata"]["labels"]["autoscaler_count"]) - 1)
					pykube.StatefulSet(api, sfs.obj).update()
					os.system('echo "[INFO] Seelp StatefulSet %s replicas %s, attempts %s"' % (sfs.obj["metadata"]["name"], sfs.obj["spec"]["replicas"], sfs.obj["metadata"]["labels"]["autoscaler_count"]))

	os.system('echo "[INFO] StatefulSet autoscaler %s"' % (set_scaling))
	os.system('echo "Seelp %ss for next query"' % (time_query))
	time.sleep(time_query)
