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
time_query = int(dic_argv["time_query"])
name_set = dic_argv["name_set"]
type_balance = dic_argv["type_balance"]
cookie = dic_argv["cookie"].lower()

if time_query < 5:
	time_query = "5"

replicas = 0
while True:
	list_set = select_statefulset(name_set, api, namespace, type_balance, cookie)
	list_set = select_pod_form_set(api, list_set, namespace, url_heapster)
	#list_set = percent_cpu_set(list_set)

	if replicas != list_set[0]["replicas"]:
		template_render = load_singleset_template(patch_exec, list_set)

		file_conf = open('/etc/haproxy/haproxy.cfg','w')
		file_conf.write(template_render)
		file_conf.close()
		os.system('chown haproxy:haproxy /etc/haproxy/haproxy.cfg')
		os.system('service haproxy reload')

		os.system('echo [UPDATE] Changes in replicas of %s' % (name_set))
	else:
		os.system('echo [INFO] No changes in replicas of %s' % (name_set))

	replicas = list_set[0]["replicas"]
	os.system('echo "Seelp %ss for next query"' % (time_query))
	time.sleep(time_query)#!/usr/bin/python

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
time_query = int(dic_argv["time_query"])
name_set = dic_argv["name_set"]
type_balance = dic_argv["type_balance"]
cookie = dic_argv["cookie"].lower()

if time_query < 5:
	time_query = "5"

replicas = 0
while True:
	list_set = select_statefulset(name_set, api, namespace, type_balance, cookie)
	list_set = select_pod_form_set(api, list_set, namespace, url_heapster)
	#list_set = percent_cpu_set(list_set)

	if replicas != list_set[0]["replicas"]:
		template_render = load_singleset_template(patch_exec, list_set)

		file_conf = open('/etc/haproxy/haproxy.cfg','w')
		file_conf.write(template_render)
		file_conf.close()
		os.system('chown haproxy:haproxy /etc/haproxy/haproxy.cfg')
		os.system('service haproxy reload')

		os.system('echo [UPDATE] Changes in replicas of %s' % (name_set))
	else:
		os.system('echo [INFO] No changes in replicas of %s' % (name_set))

	replicas = list_set[0]["replicas"]
	os.system('echo "Seelp %ss for next query"' % (time_query))
	time.sleep(time_query)