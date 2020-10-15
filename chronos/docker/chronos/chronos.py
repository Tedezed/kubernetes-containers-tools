#!/usr/bin/python3
# -*- coding: utf-8 -*-

# By: Juan Manuel Torres (Tedezed)
# Source: https://github.com/Tedezed
# Mail: juanmanuel.torres@aventurabinaria.es

import string, logging, subprocess, logging, random, yaml
from kubernetes import client, config
from os import path, getlogin, system, listdir, getuid, environ
from pwd import getpwuid
from sys import argv
from copy import deepcopy
from base64 import b64decode
from deepdiff import DeepDiff
from jinja2 import Environment, FileSystemLoader
from time import sleep
from datetime import datetime, timedelta
from psutil import disk_usage

from sendmail import *
from squirrel_integration import *

from module_control import *

class chronos:
    ruta_exec=path.dirname(path.realpath(__file__))
    directory_backups="backups"
    path_conf="/secrets"
    v1=None
    extv1beta1=None
    bash_bold='\033[1m'
    bash_none='\033[00m'

    def __init__(self, input_dic_argv, input_debug):

        self.dic_argv = input_dic_argv
        self.backup_label = "backup"

        def argument_to_dic(list):
            dic = {}
            for z in list:
                dic[z[0]] = z[1]
            return dic

        list_argv = []
        argv.remove(argv[0])
        for elements in argv:
            var_input = elements.split("=")
            if len(var_input) == 1 or var_input[1] == '':
                raise NameError('[ERROR] Invalid Arguments [python example.py var="text"]')
            list_argv.append(var_input)
        self.dic_argv = argument_to_dic(list_argv)

        if self.dic_argv["mode"] == "databases":
            self.name_configmap="databases-conf"
        else:
            self.name_configmap="disks-conf"

        try:
            self.dic_argv["subtract_days"]
        except:
            self.dic_argv["subtract_days"] = "10"

        # Load Config
        if not path.exists('/.dockerenv'):
            config.load_kube_config(config_file='/home/%s/.kube/config' % (getpwuid(getuid()).pw_name))
        else:
            config.load_incluster_config()

        # Define API
        self.v1 = client.CoreV1Api()
        self.extv1beta1 = client.ExtensionsV1beta1Api()

        # Log
        logging.basicConfig(filename='%s/%s/kube-backup.log' % (\
          self.ruta_exec, \
          self.directory_backups \
        ), level=logging.INFO)
        self.chronos_logging = logging

        # Squirrel integration
        self.sqin = squirrel_integration(self)

        # Debug: debug disable send_mail
        self.debug = input_debug

    def id_generator(self, size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))
    
    def path_check(self, input_path):
        if not path.isdir(input_path):
            system("mkdir %s" % (input_path))

    def path_service(self, service):
        out_path_database = "%s/%s/%s" % (self.ruta_exec, self.directory_backups, service)
        self.path_check(out_path_database)
        return out_path_database

    def path_backup(self, input_path_database, input_database):
        out_path_backup = "%s/%s" % (input_path_database, input_database)
        self.path_check(out_path_backup)
        return out_path_backup
    
    def execute_command(self, command):
        self.chronos_logging.warning("Command: %s" % command)
        direct_output = subprocess.call(str(command), shell=True)
        if direct_output == 0:
            print("[INFO] Command susscess")
            self.chronos_logging.warning("[INFO] Command susscess")
        else:
            self.chronos_logging.error("[ERROR] Command error %s" % (command))
            send_mail("[ERROR BACKUP] %s" % command, self.debug)

    def check_disk(self, check_path = '/'):
        obj_Disk = disk_usage(check_path)

        total = int(obj_Disk.total / (1024.0 ** 3))
        used = int(obj_Disk.used / (1024.0 ** 3))
        free = int(obj_Disk.free / (1024.0 ** 3))
        percent_used = int(obj_Disk.percent)

        status_disk = """Check: %s
        Total disk: %sG
        Used: %sG
        Free: %sG
        Percent used: %s%%
        """ % (check_path, total, used, free, percent_used)

        print(status_disk)
        warning_percent = 80
        critical_percent = 90
        if percent_used > warning_percent:
            status = "WARNING"
        elif percent_used > critical_percent:
            status = "CRITICAL"

        if percent_used > warning_percent and environ['EMAIL_MODE'] != "OFF":
            print("Try send email...")
            send_mail("[BACKUP] Status %s" % status, status_disk, self.debug)

    def get_configmap(self, name_conf, conf_mode):
        ret = self.v1.list_config_map_for_all_namespaces(watch=False)
        if conf_mode == "configmap":
            for i in ret.items:
                if i.metadata.name == name_conf:
                    data = i.data
        elif conf_mode == "api":
            patch_conf = "%s/%s/%s.yaml" % (self.path_conf, self.dic_argv["mode"], name_conf)
            print("[INFO] Read conf from %s" % conf_mode)
            stream = open(patch_conf, "r")
            text_yaml = stream.read()
            text_yaml = text_yaml.replace('\t', '   ')
            file_yaml = yaml.load(text_yaml)
            stream.close()
            data = file_yaml["data"]
        else:
            print("[ERROR] Conf_mode not found.")
            exit()

        if name_conf == "kube-backup-cron-configmap":
            list_db = []
            for d in data:
                dic_data = {}
                name = str(d)
                dic_data["job_name"] = name
                data_n = data[name].split("\n")
                list_data = []
                for n in data_n:
                    dic_data_split = {}
                    data_split = n.split("=")
                    try:
                        if data_split[1] == "database_list":
                            dic_data[str(data_split[0])] = data_split[1].split("&")
                        else:
                            dic_data[str(data_split[0])] = data_split[1].replace(" ", "")
                    except:
                        pass
                list_db.append(dic_data)
            return list_db

        if name_conf == "kube-snapshot-cron-configmap":
            list_disk = []
            for d in data:
                dic_data = {}
                name = str(d)
                dic_data["name_disk"] = name
                data_n = data[name].split("\n")
                list_data = []
                for n in data_n:
                    dic_data_split = {}
                    data_split = n.split("=")
                    try:
                        dic_data[str(data_split[0])] = data_split[1]
                    except:
                        pass
                list_disk.append(dic_data)
            return list_disk

    def safe_list_get(self, l, idx, default):
      try:
        return l[idx]
      except IndexError:
        return default

    def get_selector_from_service(self, name, namespace = ""):
        services = self.v1.list_service_for_all_namespaces(watch=False)
        for s in services.items:
            if s.metadata.name == name and s.metadata.namespace == namespace:
                try:
                    return s.spec.selector
                except:
                    return {'not-found': 'true'}

    def get_svc_ip(self, name_svc, namespace_svc):
        ret = self.v1.list_service_for_all_namespaces(watch=False)
        for i in ret.items:
            if i.metadata.name.replace(" ", "") == name_svc.replace(" ", "")\
             and i.metadata.namespace.replace(" ", "") == namespace_svc.replace(" ", ""):
                return i.spec.cluster_ip

    def get_ip_from_pod(self, svc_labels, namespace):
        pod = self.v1.list_pod_for_all_namespaces(watch=False)
        # Only for pods
        list_ip_pod = []
        for p in pod.items:
            if p.metadata.namespace == namespace:
                key_search = None
                if svc_labels == p.metadata.labels:
                    key_search = True
                else:
                    for key in svc_labels.keys():
                        if svc_labels.get(key, 'False_dic1') == p.metadata.labels.get(key, 'False_dic2') \
                          and (key_search or key_search == None):
                            key_search = True
                        else:
                            key_search = False
                if key_search:
                    list_ip_pod.append(p.status.pod_ip)
        return list_ip_pod

    def enrich_list_databases(self, list_db):
        docker_env = path.exists('/.dockerenv')
        for idx, db in enumerate(list_db):
            if not docker_env:
                host = db["job_name"]
            else:
                try:
                    # Try IP from Pod
                    ip_error = "169.254.1.10"
                    svc_labels = self.get_selector_from_service(db["job_name"], db["namespace"])
                    svc_ip_list = self.get_ip_from_pod(svc_labels, db["namespace"])
                    #host = safe_list_get(svc_ip_list,0,ip_error)
                    host = svc_ip_list[0]
                except Exception as e:
                    error = '[Error] Not get IP from Pod, try get IP from SVC'
                    print(error)
                    logging.error(error)

                    # Try IP from SVC
                    host = self.get_svc_ip(db["job_name"], db["namespace"])
            
            list_db[idx]["host"] = host

        return list_db

    def drop_dir_datetime(self, now_datetime, ruta_backup):
        drop_datetime = now_datetime - timedelta(days=int(self.dic_argv["subtract_days"]))
        for file in listdir(ruta_backup):
            file_date = ""
            file_split = file.split("___")
            try:
                file_date = file_split[1]
                key = True
            except Exception as e:
                key = False
                print(e)
                logging.error(e)

            if datetime.strptime(file_date, "%Y-%m-%d").strftime("%Y-%m-%d") <= drop_datetime.strftime("%Y-%m-%d") \
                    and key:
                logging.warning("[INFO] [%s] Drop file %s" % (now_datetime, file))
                print("[INFO] [%s] Drop file %s" % (now_datetime, file))
                system("rm -f %s/%s" % (ruta_backup, file))

    def start_chronos(self):
        now_datetime = datetime.now()
        
        module = main_module(self, self.dic_argv["mode"], now_datetime, self.chronos_logging, \
                                    self.debug)

        print("[INFO] Conf mode %s" % self.dic_argv["conf_mode"])
        if self.dic_argv["conf_mode"] == "api":
            # Mode API
            list_db = self.sqin.get_secrets()
            if self.dic_argv["mode"] == "databases":
                input_list = self.enrich_list_databases(list_db)
            else:
                input_list = module.module_custom_job_list()
        else:
            # Mode Configmap
            try:
                input_list = self.get_configmap(self.name_configmap, self.dic_argv["conf_mode"])
            except Exception as e:
                print("[ERROR] (read local configmap) %s" % e)
                input_list = []

        try:
            module.module_exec_list_job(input_list)
        except Exception as e:
            error = '[ERROR] [%s] (start_modules)' % (now_datetime)
            print(error, e)
            self.chronos_logging.error(error, e)
            send_mail(error, error, self.debug)

