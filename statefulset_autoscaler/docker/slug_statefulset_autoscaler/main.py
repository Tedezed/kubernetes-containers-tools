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

import time, requests, pykube, json, os, sys, datetime
from tools import *

# Example execution
# python main.py namespace="default" url_heapster="http://heapster/api/v1/model" slug-autoscaler/autoscaler_count="5" time_query="10"

os.system('echo "[%s][START] Slug StatefulSet Autoscaler v.2.0"' % (datetime.datetime.now()))
patch_exec = os.path.dirname(os.path.realpath(__file__)) + "/"

if not os.path.exists('/.dockerenv'):
	home = str(os.path.expanduser('~'))
	api = pykube.HTTPClient(pykube.KubeConfig.from_file("%s/.kube/config-slug" % home))
else:
	api = pykube.HTTPClient(pykube.KubeConfig.from_service_account())

# Arguments
list_argv=[]
sys.argv.remove(sys.argv[0])
for elements in sys.argv:
	variable_entrada = elements.split("=")
	if len(variable_entrada) == 1 or variable_entrada[1] == '':
		raise NameError('[ERROR] Invalid Arguments [python example.py var="text"]')
	list_argv.append(variable_entrada)

dic_argv = argument_to_dic(list_argv)
url_heapster = dic_argv["url_heapster"]
autoscaler_count = dic_argv["autoscaler_count"]
time_query = int(dic_argv["time_query"])

# Min time_querys
if int(autoscaler_count) < 3:
	autoscaler_count = "3"
if time_query < 5:
	time_query = "5"

while True:
	namespace_list = pykube.Namespace.objects(api)
	for namespace in namespace_list:
		list_set = select_statefulset(api, namespace)

		if list_set:
			list_set = select_pod_form_set(api, list_set, namespace, url_heapster)
			list_set = percent_cpu_set(list_set)

			pre_set = pykube.StatefulSet.objects(api)
			change = 0
			set_scaling = 0
			for sfs in pre_set.response['items']:
				if str(sfs["metadata"]["namespace"]) == str(namespace):
					print "[%s][INFO]Process sts of namespace %s" % (datetime.datetime.now(),namespace)

					# Clean json to pod
					sfs['metadata'].pop('resourceVersion', None)
					sfs['metadata'].pop('creationTimestamp', None)

					# Start
					for setfull in list_set:
						os.system('echo "[%s][STS] %s - CPU: NOW %s, MAX %s, MIN %s"' \
							% (datetime.datetime.now(), sfs["metadata"]["name"], str(setfull["percent_cpu"])+"%", \
								str(setfull["autoscaler_percent_cpu"])+"%", \
								str(setfull["autoreduce_percent_cpu"])+"%"))
						os.system('echo "[%s][STS] %s - REPLICAS: NOW %s, MAX %s, MIN %s"' \
							% (datetime.datetime.now(), sfs["metadata"]["name"], \
								sfs["spec"]["replicas"], \
								setfull["max_replicas"], \
								setfull["min_replicas"]))
						replicas = int(sfs["spec"]["replicas"])

						try:
							if sfs["spec"]["template"]["metadata"]["annotations"]["slug-autoscaler/autoscaler_count"] == "0":
								# Autoscale
								if sfs["metadata"]["name"] == setfull["name"] \
								  and int(setfull["autoscaler_percent_cpu"]) <= int(setfull["percent_cpu"]):
									sfs["spec"]["replicas"] = replicas + 1
									sfs["spec"]["template"]["metadata"]["annotations"]["slug-autoscaler/autoscaler_count"] = autoscaler_count
									set_scaling += 1
								# Autoreduce Normal
								elif sfs["metadata"]["name"] == setfull["name"] \
								  and int(setfull["autoreduce_percent_cpu"]) >= int(setfull["percent_cpu"]) \
								  and setfull["autoreduce_normal"].lower() == "true":
									sfs["spec"]["replicas"] = replicas - 1
									sfs["spec"]["template"]["metadata"]["annotations"]["slug-autoscaler/autoscaler_count"] = autoscaler_count
									set_scaling += 1
								if set_scaling != 0:
									#print "%s <= %s and %s >= %s "  % (setfull["min_replicas"], sfs["spec"]["replicas"],\
									# setfull["max_replicas"], sfs["spec"]["replicas"])
									if int(setfull["min_replicas"]) <= int(sfs["spec"]["replicas"]) \
									  and int(setfull["max_replicas"]) >= int(sfs["spec"]["replicas"]):
										pykube.StatefulSet(api, sfs).update()
										os.system('echo "[%s][AUTOSCALING] %s replicas: min %s max %s "' \
										  % (datetime.datetime.now(),sfs["metadata"]["name"], setfull["min_replicas"],\
										     setfull["max_replicas"]))
										os.system('echo "[%s][AUTOSCALING] %s replicas: %s to %s "' \
										  % (datetime.datetime.now(),sfs["metadata"]["name"], replicas, sfs["spec"]["replicas"]))
										change += 1
							else:
								# Reduce only slug-autoscaler/autoscaler_count
								sfs["spec"]["template"]["metadata"]["annotations"]["slug-autoscaler/autoscaler_count"] = str(\
								  int(sfs["spec"]["template"]["metadata"]["annotations"]["slug-autoscaler/autoscaler_count"]) - 1\
								)
								os.system('echo "[%s][INFO] Seelp STS %s replicas %s, attempts %s"' \
								  % (datetime.datetime.now(),sfs["metadata"]["name"], sfs["spec"]["replicas"], \
								  	  sfs["spec"]["template"]["metadata"]["annotations"]["slug-autoscaler/autoscaler_count"]))
								if int(setfull["min_replicas"]) <= int(sfs["spec"]["replicas"]) \
								  and int(setfull["max_replicas"]) >= int(sfs["spec"]["replicas"]):
									pykube.StatefulSet(api, sfs).update()
						except Exception as e:
							print "Exception: %s" % e
			#os.system('echo "[%s][INFO] STS autoscaler %s"' % (datetime.datetime.now(),change))
	os.system('echo "[%s][INFO] Seelp %ss for next query"' % (datetime.datetime.now(),time_query))
	time.sleep(time_query)