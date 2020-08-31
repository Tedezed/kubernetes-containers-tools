#!/usr/bin/python
# -*- coding: utf-8 -*-

# Source: https://github.com/Tedezed
# Mail: juanmanuel.torres@aventurabinaria.es

# client.configuration.host

import smtplib
from email.mime.text import MIMEText
import googleapiclient.discovery, subprocess, logging, string, random, yaml
import psycopg2, mysql.connector
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

from gcloud_tools import *
from squirrel_integration import *

class kube_init:
    ruta_exec=path.dirname(path.realpath(__file__))
    directory_backups="backups"
    name_configmap_backup="kube-backup-cron-configmap"
    name_configmap_snapshot="kube-snapshot-cron-configmap"
    ruta_conf="/secrets"
    v1=None
    extv1beta1=None
    bash_bold='\033[1m'
    bash_none='\033[00m'

    def __init__(self):

        def argument_to_dic(list):
            dic = {}
            for z in list:
                dic[z[0]] = z[1]
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
            config.load_kube_config(config_file='/home/%s/.kube/config_liberty_guadaltech' % (getpwuid(getuid()).pw_name))
            # config.load_kube_config()
            # config.load_kube_config(config_file='%s/credentials/config' % (self.ruta_exec))
        else:
            config.load_incluster_config()

        # Define API
        self.v1 = client.CoreV1Api()
        self.extv1beta1 = client.ExtensionsV1beta1Api()

        # Log
        logging.basicConfig(filename='%s/%s/kube-backup.log' % (self.ruta_exec, self.directory_backups), level=logging.INFO)

        # Squirrel integration
        self.sqin = squirrel_integration(self)

    def id_generator(self, size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

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

        print status_disk
        warning_percent = 80
        critical_percent = 90
        if percent_used > warning_percent:
            status = "WARNING"
        elif percent_used > critical_percent:
            status = "CRITICAL"

        if percent_used > warning_percent and environ['EMAIL_MODE'] != "OFF":
            print "Try send email..."
            self.send_mail("[SLUG-BACKUP] Status %s" % status, status_disk)

    def send_mail(self, subject, body):
        send_to = environ['EMAIL_SEND_TO'].split(",")
        email_mode = environ['EMAIL_MODE']
        email_server = environ['EMAIL_SERVER']
        email_port = environ['EMAIL_PORT']
        email_user = environ['EMAIL_USER']
        email_password = str(environ['EMAIL_PASSWORD'].encode('utf-8'))

        server = smtplib.SMTP(email_server, email_port)
        server.ehlo()
        server.starttls()
        server.ehlo()
        try:
            server.login(email_user, email_password)

            msg = MIMEText(body, "html")
            msg['Subject'] = subject
            msg['From'] = email_user
            msg['To'] = ', '.join(send_to)

            try:
                for s in send_to:
                    server.sendmail(email_user, s, msg.as_string())
                print '[INFO] Email sent!'
            except Exception as e:  
                print '[ERROR] Email: %s' % (e)
        except Exception as e:  
                print '[ERROR] %s' % (e)

    def check(self, name_conf, conf_mode):
        ret = self.v1.list_config_map_for_all_namespaces(watch=False)
        key_data_found = False
        now_datetime = datetime.now()

        print "[INFO] Conf mode %s" % conf_mode
        if conf_mode == "conf-map":
            for i in ret.items:
                if i.metadata.name == name_conf:
                    data = i.data
                    key_data_found = True

            if key_data_found:
                return key_data_found
            else:
                print "[ERROR] [%s] Configmap %s not found" % (now_datetime, name_conf)
                return key_data_found

        elif conf_mode == "secret":
            return True
        else:
            print "[ERROR] Conf mode %s not found" % conf_mode
            return False

    def get_configmap(self, name_conf, conf_mode):
        ret = self.v1.list_config_map_for_all_namespaces(watch=False)
        if conf_mode == "conf-map":
            for i in ret.items:
                if i.metadata.name == name_conf:
                    data = i.data
        elif conf_mode == "secret":
            patch_conf = "%s/%s/%s.yaml" % (self.ruta_conf, self.dic_argv["mode"], name_conf)
            print "[INFO] Read conf from %s" % conf_mode
            stream = open(patch_conf, "r")
            text_yaml = stream.read()
            text_yaml = text_yaml.replace('\t', '   ')
            file_yaml = yaml.load(text_yaml)
            stream.close()
            data = file_yaml["data"]
        else:
            print "[ERROR] Conf_mode not found."
            exit()

        if name_conf == "kube-backup-cron-configmap":
            list_db = []
            for d in data:
                dic_data = {}
                name = str(d)
                dic_data["name_svc"] = name
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
        list_svc = []
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

    def bakup_sql(self, db, now_datetime):
        try:
            if not path.exists('/.dockerenv'):
                host = db["name_svc"]
            else:
                try:
                    # Try IP from Pod
                    ip_error = "169.254.1.10"
                    svc_labels = self.get_selector_from_service(db["name_svc"], db["namespace"])
                    svc_ip_list = self.get_ip_from_pod(svc_labels, db["namespace"])
                    #host = safe_list_get(svc_ip_list,0,ip_error)
                    host = svc_ip_list[0]
                except Exception as e:
                    error = '[Error] Not get IP from Pod, try get IP from SVC'
                    print error
                    logging.error(error)

                    # Try IP from SVC
                    host = self.get_svc_ip(db["name_svc"], db["namespace"])


            print '[START] Service: %s, Host: %s' % (db["name_svc"], host)

            if db["type"] == "postgres":
                db_user = db["POSTGRES_USER"]
                db_user_pass = str(db["POSTGRES_PASSWORD"].encode('utf-8'))
                db_port = db["port"]
                conn = psycopg2.connect(dbname='postgres', user=db_user, \
                                    host=host, password=db_user_pass, port=db_port)
                key = True
            elif db["type"] == "mysql":
                db_user = db["MYSQL_USER"]
                db_user_pass = str(db["MYSQL_PASSWORD"].encode('utf-8'))
                db_port = db["port"]
                conn = mysql.connector.connect(database='', user=db_user, \
                                    host=host, password=db_user_pass, port=db_port)
                key = True
            else:
                error = '[Error] Not valid database type found'
                print error
                logging.error(error)
                #raise ValueError(error)
                self.send_mail("[ERROR SLUG-BACKUP] %s %s" % (db["name_svc"], host), error)

        except Exception as e:
            key = False
            error = '[ERROR] [%s] host %s not found ' % (now_datetime, db["name_svc"])
            print "host: %s, user: %s, pass: %s, port: %s" % (host, db_user, db_user_pass, db_port)
            print error
            print e
            logging.error(error)
            logging.error(e)
            self.send_mail("[ERROR SLUG-BACKUP] %s" % (db["name_svc"]), error)

        if key:
            logging.info('[INFO] [%s] Connect to %s ' % (now_datetime, db["name_svc"]))
            cur = conn.cursor()
            if db["type"] == "postgres":
                cur.execute("""SELECT datname FROM pg_database""")
            elif db["type"] == "mysql":
                cur.execute("""SHOW DATABASES""")

            rows = cur.fetchall()
            for r in rows:
                if r[0] not in ["template", "template0", "template1" ,"information_schema", "postgres", "mysql", "performance_schema"]:

                    ruta_database = "%s/%s/%s" % (self.ruta_exec, self.directory_backups, db["name_svc"])
                    if not path.isdir(ruta_database):
                        system("mkdir %s" % (ruta_database))

                    ruta_backup = "%s/%s" % (ruta_database, str(r[0]))
                    if not path.isdir(ruta_backup):
                        system("mkdir %s" % (ruta_backup))

                    print "[INFO] Dump %s" % r
                    if db["type"] == "postgres":
                        dump_command = 'pg_dump -Fc --dbname=postgresql://%s:%s@%s:%s/%s > %s/%s___%s___%s.dump' % \
                                       (db["POSTGRES_USER"], str(db["POSTGRES_PASSWORD"].encode('utf-8')), host, db["port"], str(r[0]), \
                                        ruta_backup, str(r[0]), now_datetime.strftime("%Y-%m-%d"), self.id_generator())
                    elif db["type"] == "mysql":
                        dump_command = 'mysqldump -u %s -p%s -h %s -P %s --databases %s > %s/%s___%s___%s.dump' % \
                                       (db["MYSQL_USER"], str(db["MYSQL_PASSWORD"].encode('utf-8')), host, db["port"], str(r[0]), \
                                        ruta_backup, str(r[0]), now_datetime.strftime("%Y-%m-%d"), self.id_generator())

                    # try:
                    logging.warning("Command: %s" % dump_command)
                    var = direct_output = subprocess.call(str(dump_command), shell=True)
                    if var == 0:
                        print "[INFO] [%s] Backup %s..." % (now_datetime, r[0])
                        logging.warning("[INFO] [%s] Backup %s..." % (now_datetime, r[0]))
                    else:
                        logging.error("[ERROR] [%s] in backup %s" % (now_datetime, r[0]))
                        self.send_mail("[ERROR SLUG-BACKUP] %s" % str(r[0]), ruta_backup)

                    self.drop_dir_datetime(now_datetime, ruta_backup)
        else:
            print "[INFO] key service False"

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
                print e
                logging.error(e)

            if datetime.strptime(file_date, "%Y-%m-%d").strftime("%Y-%m-%d") <= drop_datetime.strftime("%Y-%m-%d") \
                    and key:
                logging.warning("[INFO] [%s] Drop file %s" % (now_datetime, file))
                print "[INFO] [%s] Drop file %s" % (now_datetime, file)
                system("rm -f %s/%s" % (ruta_backup, file))

    def date_drop_snapshot(self, now_datetime):
        drop_datetime = now_datetime - timedelta(days=int(self.dic_argv["subtract_days"]))
        print "[INFO] Checking snapshot that are on or out the erase date: %s" % drop_datetime
        list_snapshot = self.gtools.list_snapshot(self.dic_argv["project"])
        if list_snapshot != None:
            for s in list_snapshot:
                file_date = ""
                try:
                    if "---" in s["name"]:
                        name_split = s["name"].split("---")
                        name_date = name_split[1]
                        if datetime.strptime(name_date, "%Y-%m-%d").strftime("%Y-%m-%d") <= drop_datetime.strftime("%Y-%m-%d"):
                            logging.warning("[INFO] [%s] Drop snapshot %s" % (now_datetime, s["name"]))
                            print "[INFO] [%s] Drop snapshot %s" % (now_datetime, s["name"])
                            self.gtools.delete_snapshot(self.dic_argv["project"],s["name"])
                except Exception as e:
                    key = False
                    print e
                    logging.error(e)
        else:
            print "[INFO] Not found snapshot that are on or out the erase date: %s" % drop_datetime

    def fusion_list_dbs(self, list_db1, list_db2):
        # list_db2 prevails over list_db1
        list_end = []
        if list_db1:
            for db1 in list_db1:
                found_in_list_db2 = False
                for db2 in list_db2:
                    #print("%s %s %s %s" % (db1["name_svc"], db2["name_svc"], db2["namespace"], db2["namespace"]))
                    if db1["name_svc"] == db2["name_svc"] and db2["namespace"] == db2["namespace"]:
                        found_in_list_db2 = True
                if found_in_list_db2:
                    list_end.append(db2)
                else:
                    list_end.append(db1)
            return list_end
        else:
            return list_db2

    def fusion_list_dbs_v2(self, list_db1, list_db2):
        list_end = []
        print "[INFO] Init fusion_list_dbs_v2"
        print list_db1
        print list_db2
        if list_db1:

            # Add only equal and list1
            for db1 in list_db1:
                found_db1 = False
                for db2 in list_db2:
                    if db1["name_svc"] == db2["name_svc"] and db2["namespace"] == db2["namespace"]:
                        list_end.append(db1)
                        found_db1 = True
                if not found_db1:
                    list_end.append(db1)

            # Add only in list2
            for db2 in list_db2:
                found_db2 = False
                for db1 in list_db1:
                    if db1["name_svc"] == db2["name_svc"] and db2["namespace"] == db2["namespace"]:
                        found_db2 = True
                if not found_db2:
                    list_end.append(db2)

            print "[INFO] (fusion_list_dbs_v2) Use list 1 and 2"
            print list_end
            return list_end
        else:
            print "[INFO] (fusion_list_dbs_v2) Only use list 2"
            print list_db2
            return list_db2

    def start_kube_backup(self):
        list_db_secrets = self.sqin.get_secrets()
        now_datetime = datetime.now()
        try:
            list_db_configmap = self.get_configmap(self.name_configmap_backup, self.dic_argv["conf_mode"])
        except Exception as e:
            print "[ERROR] %s" % e
            list_db_configmap = []
        #list_db = self.fusion_list_dbs_v2(list_db_configmap, list_db_secrets)
        list_db = self.fusion_list_dbs_v2(list_db_secrets, list_db_configmap)
        for db in list_db:
            #print db
            self.bakup_sql(db, now_datetime)

    def snapshot_op(self, list_disk):
        now_datetime = datetime.now()
        for disk in list_disk:
            if len(disk["name_disk"]) > 45:
                name_snapshot = disk["name_disk"][0:45] + "---" + now_datetime.strftime("%Y-%m-%d")
            else:
                name_snapshot = disk["name_disk"] + "---" + now_datetime.strftime("%Y-%m-%d")

            logging.warning("[INFO] [%s] Create snapshot %s" % (now_datetime, name_snapshot))
            print "[INFO] [%s] Create snapshot %s" % (now_datetime, name_snapshot)
            try:
                self.gtools.disk_to_snapshot(self.dic_argv["project"], disk["zone"], disk["name_disk"], name_snapshot)
            except Exception as e:
                print e
                logging.error(e)
        self.date_drop_snapshot(now_datetime)

    def snapshot(self):
        self.gtools = gcloud_tools()
        list_disk = self.get_configmap(self.name_configmap_snapshot, self.dic_argv["conf_mode"])
        
        if list_disk:
            self.snapshot_op(list_disk)

    def snapshot_filter_label(self):
        self.gtools = gcloud_tools()
        list_disk_gcp = self.gtools.list_disks(self.dic_argv["project"], self.dic_argv["zone"])

        list_disk = []
        for disk in list_disk_gcp:
            disk_labels = disk.get("labels", [])
            disk_label_backup = "false"
            for l in disk_labels:
                if l == "backup":
                    disk_label_backup = disk_labels[l]
            if disk["status"] == "READY" and disk_label_backup.lower() ==  "true":
                dict_disk = {"name_disk": disk["name"], "zone": self.dic_argv["zone"]}
                list_disk.append(dict_disk)

        if list_disk:
            self.snapshot_op(list_disk)


## Start ##

def argument_to_dic(list):
    dic = {}
    for z in list:
        dic[z[0]] = z[1]
    return dic


def main():
    list_argv = []
    argv_ext = deepcopy(argv)

    argv_ext.remove(argv_ext[0])
    for elements in argv_ext:
        variable_entrada = elements.split("=")
        if len(variable_entrada) == 1 or variable_entrada[1] == '':
            raise NameError('[ERROR] Invalid Arguments [python example.py var="text"]')
        list_argv.append(variable_entrada)
    dic_argv = argument_to_dic(list_argv)

    kluster = kube_init()
    kluster.check_disk("/slug-backup-db-cron/backups")
    if dic_argv.get("mode", False) == "backup":
        if kluster.check(kluster.name_configmap_backup, dic_argv["conf_mode"]):
            kluster.start_kube_backup()
    elif dic_argv.get("mode", False) == "snapshot":
        if kluster.check(kluster.name_configmap_snapshot, dic_argv["conf_mode"]):
            try:
                kluster.snapshot()
            except Exception as error:
                print "[ERROR] snapshot_label %s" % str(error)
                logging.error(error)
                kluster.send_mail("[ERROR SLUG-BACKUP] Mode %s" % ("snapshot"), str(error).replace("<","").replace(">",""))
            
    elif dic_argv.get("mode", False) == "snapshot_label":
        try:
            kluster.snapshot_filter_label()
        except Exception as error:
            print "[ERROR] snapshot_label %s" % str(error)
            logging.error(error)
            kluster.send_mail("[ERROR SLUG-BACKUP] Mode %s" % ("snapshot_label"), str(error).replace("<","").replace(">",""))

    else:
        print "[ERROR] Mode not found"


if __name__ == '__main__':
    # Start
    main()
