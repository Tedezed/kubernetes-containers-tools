#!/usr/bin/python
# -*- coding: utf-8 -*-

# Source: https://github.com/Tedezed
# Mail: juanmanuel.torres@aventurabinaria.es

#client.configuration.host


from kubernetes import client, config
from os import path, getlogin, system, listdir
from sys import argv
import subprocess
from base64 import b64decode
from deepdiff import DeepDiff
from jinja2 import Environment, FileSystemLoader
from time import sleep
import psycopg2
import logging
import string
import random
from datetime import datetime, timedelta

class kube_init:
	ruta_exec = path.dirname(path.realpath(__file__))
	v1 = None
	extv1beta1 = None
	bash_bold='\033[1m'
	bash_none='\033[00m'

	def __init__(self):

		def argument_to_dic(list):
			dic = {}
			for z in list:
				dic[z[0]]=z[1]
			return dic

		list_argv = []
		argv.remove(argv[0])
		for elements in argv:
			variable_entrada = elements.split("=")
			if len(variable_entrada) == 1 or variable_entrada[1] == '':
				raise NameError('[ERROR] Invalid Arguments [python example.py var="text"]')
			list_argv.append(variable_entrada)
		self.dic_argv = argument_to_dic(list_argv)

		try:
			self.dic_argv["subtract_days"]
		except:
			self.dic_argv["subtract_days"] = "10"

		# Load Config
		if not path.exists('/.dockerenv'):
			config.load_kube_config(config_file='/home/%s/.kube/config_liberty' % (getlogin()))
			#config.load_kube_config()
			#config.load_kube_config(config_file='%s/credentials/config' % (self.ruta_exec))
		else:
			config.load_incluster_config()

		# Define API
		self.v1 = client.CoreV1Api()
		self.extv1beta1 = client.ExtensionsV1beta1Api()

		#Log
		logging.basicConfig(filename='/slug-backup-db-cron/backups/kube-backup.log',level=logging.INFO)

	def id_generator(self, size=6, chars=string.ascii_uppercase + string.digits):
		return ''.join(random.choice(chars) for _ in range(size))

	def get_configmap(self):
		ret = self.v1.list_config_map_for_all_namespaces(watch=False)

		for i in ret.items:
			if i.metadata.name == "kube-backup-cron-configmap":
				data = i.data

		list_db=[]
		for d in data:
			dic_data={}
			name=str(d)
			dic_data["name_svc"]=name
			data_n=data[name].split("\n")
			list_data=[]
			for n in data_n:
				dic_data_split={}
				data_split=n.split("=")
				try:
					if data_split[1] == "database_list":
						dic_data[str(data_split[0])]=data_split[1].split("&")
					else:
						dic_data[str(data_split[0])]=data_split[1]
				except:
					pass
			list_db.append(dic_data)
		return list_db

	def get_svc_ip(self, name_svc, namespace_svc):
		ret = self.v1.list_service_for_all_namespaces(watch=False)
		for i in ret.items:
			if i.metadata.name == name_svc and i.metadata.namespace == namespace_svc:
				return i.spec.cluster_ip

	def bakup_postgres(self, db, now_datetime):
		try:
			if not path.exists('/.dockerenv'):
				host = db["name_svc"]
			else:
				host = self.get_svc_ip(db["name_svc"], db["namespace"])

			conn = psycopg2.connect(dbname='postgres', user=db["POSTGRES_USER"],\
				 host=host, password=db["POSTGRES_PASSWORD"], port=db["port"])
			key=True
		except Exception as e:
			key=False
			error = '[%s] [ERROR] host %s not found ' % (now_datetime, db["name_svc"])
			print error
			logging.error(error)
			logging.error(e)

		if key:
			logging.info('[%s] [INFO] Connect to %s ' % (now_datetime, db["name_svc"]))
			cur = conn.cursor()
			cur.execute("""SELECT datname FROM pg_database""")
			rows = cur.fetchall()
			for r in rows:
				if "template" not in r[0]:

					ruta_database="%s/backups/%s" % (self.ruta_exec, db["name_svc"])
					if not path.isdir(ruta_database):
						system("mkdir %s" % (ruta_database))

					ruta_backup = "%s/%s" % (ruta_database, str(r[0]))
					if not path.isdir(ruta_backup):
						system("mkdir %s" % (ruta_backup))
					
					dump_command = 'pg_dump -Fc --dbname=postgresql://%s:%s@%s:%s/%s > %s/%s___%s___%s.dump' %\
					 (db["POSTGRES_USER"], db["POSTGRES_PASSWORD"], host, db["port"], str(r[0]),\
					 ruta_backup, str(r[0]), now_datetime.strftime("%Y-%m-%d"), self.id_generator())

					#try:
					var = direct_output = subprocess.call(dump_command, shell=True)
					if var == 0:
						print "[%s] [INFO] Backup %s" % (now_datetime, r[0])
						logging.warning("[%s] [INFO] Backup %s" % (now_datetime, r[0]))
					else:
						logging.error("[%s] [ERROR] in backup %s" % (now_datetime, r[0]))

					self.drop_dir_datetime(now_datetime, ruta_backup)

	def drop_dir_datetime(self, now_datetime, ruta_backup):
		drop_datetime = now_datetime - timedelta(days=int(self.dic_argv["subtract_days"]))
		for file in listdir(ruta_backup):
			file_split = file.split("___")
			try:
				file_date = file_split[1]
				key=True
			except Exception as e:
				key=False
				print e
				logging.error(e)

			if datetime.strptime(file_date, "%Y-%m-%d").strftime("%Y-%m-%d") <= drop_datetime.strftime("%Y-%m-%d") and key:
				logging.warning("[%s] [INFO] Drop file %s" % (now_datetime, file))
				print "[%s] [INFO] Drop file %s" % (now_datetime, file)
				system("rm -f %s/%s" % (ruta_backup, file))

	def start_kube_backup(self):
		now_datetime = datetime.now()
		list_db=self.get_configmap()
		for db in list_db:
			if db["type"] == "postgres":
				self.bakup_postgres(db, now_datetime)

def main():
	kluster = kube_init()
	kluster.start_kube_backup()


if __name__ == '__main__':
	#Start
	main()