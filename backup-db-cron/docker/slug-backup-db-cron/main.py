#!/usr/bin/python
# -*- coding: utf-8 -*-

# Source: https://github.com/Tedezed
# Mail: juanmanuel.torres@aventurabinaria.es

# client.configuration.host

import googleapiclient.discovery, subprocess, logging, string, random, yaml
import psycopg2, mysql.connector
from kubernetes import client, config
from os import path, getlogin, system, listdir, getuid
from pwd import getpwuid
from sys import argv
from copy import deepcopy
from base64 import b64decode
from deepdiff import DeepDiff
from jinja2 import Environment, FileSystemLoader
from time import sleep
from datetime import datetime, timedelta

class gcloud_tools:

    def __init__(self):
        self.compute = googleapiclient.discovery.build('compute', 'v1')

    def list_instances(self, project, zone):
        result = self.compute.instances().list(project=project, zone=zone).execute()
        return result.get('items', None)

    def list_disks(self, project, zone):
        result = self.compute.disks().list(project=project, zone=zone).execute()
        return result.get('items', None)

    def list_snapshot(self, project):
        result = self.compute.snapshots().list(project=project).execute()
        return result.get('items', None)

    def disk_to_snapshot(self, project, zone, disk_name, snapshot_name):
        body = {"name": snapshot_name}
        return self.compute.disks().createSnapshot(project=project, zone=zone,
                                              disk=disk_name, body=body).execute()

    def delete_snapshot(self, project, name):
        return self.compute.snapshots().delete(project=project, snapshot=name).execute()

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

    def id_generator(self, size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

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
            file_yaml = yaml.load(stream)
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
                            dic_data[str(data_split[0])] = data_split[1]
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


    def get_svc_ip(self, name_svc, namespace_svc):
        ret = self.v1.list_service_for_all_namespaces(watch=False)
        for i in ret.items:
            if i.metadata.name == name_svc and i.metadata.namespace == namespace_svc:
                return i.spec.cluster_ip

    def bakup_sql(self, db, now_datetime):
        try:
            if not path.exists('/.dockerenv'):
                host = db["name_svc"]
            else:
                host = self.get_svc_ip(db["name_svc"], db["namespace"])

            print '[INFO] Host: %s' % (host)

            if db["type"] == "postgres":
                conn = psycopg2.connect(dbname='postgres', user=db["POSTGRES_USER"], \
                                    host=host, password=db["POSTGRES_PASSWORD"], port=db["port"])
                key = True
            elif db["type"] == "mysql":
                conn = mysql.connector.connect(database='mysql', user=db["MYSQL_USER"], \
                                    host=host, password=db["MYSQL_PASSWORD"], port=db["port"])
                key = True
            else:
                error = '[Error] Not valid database type found'
                print error
                logging.error(error)
                raise ValueError(error)

        except Exception as e:
            key = False
            error = '[ERROR] [%s] host %s not found ' % (now_datetime, db["name_svc"])
            print error
            print e
            logging.error(error)
            logging.error(e)

        if key:
            logging.info('[INFO] [%s] Connect to %s ' % (now_datetime, db["name_svc"]))
            cur = conn.cursor()
            if db["type"] == "postgres":
                cur.execute("""SELECT datname FROM pg_database""")
            elif db["type"] == "mysql":
                cur.execute("""SHOW DATABASES""")

            rows = cur.fetchall()
            for r in rows:
                if "template" not in r[0]:

                    ruta_database = "%s/%s/%s" % (self.ruta_exec, self.directory_backups, db["name_svc"])
                    if not path.isdir(ruta_database):
                        system("mkdir %s" % (ruta_database))

                    ruta_backup = "%s/%s" % (ruta_database, str(r[0]))
                    if not path.isdir(ruta_backup):
                        system("mkdir %s" % (ruta_backup))

                    print "[INFO] Dump %s" % r
                    if db["type"] == "postgres":
                        dump_command = 'pg_dump -Fc --dbname=postgresql://%s:%s@%s:%s/%s > %s/%s___%s___%s.dump' % \
                                       (db["POSTGRES_USER"], db["POSTGRES_PASSWORD"], host, db["port"], str(r[0]), \
                                        ruta_backup, str(r[0]), now_datetime.strftime("%Y-%m-%d"), self.id_generator())
                    elif db["type"] == "mysql":
                        dump_command = 'mysqldump  -u %s -p%s -h %s -P %s --databases %s > %s/%s___%s___%s.dump' % \
                                       (db["MYSQL_USER"], db["MYSQL_PASSWORD"], host, db["port"], str(r[0]), \
                                        ruta_backup, str(r[0]), now_datetime.strftime("%Y-%m-%d"), self.id_generator())

                    # try:
                    var = direct_output = subprocess.call(dump_command, shell=True)
                    if var == 0:
                        print "[INFO] [%s] Backup %s" % (now_datetime, r[0])
                        logging.warning("[INFO] [%s] Backup %s" % (now_datetime, r[0]))
                    else:
                        logging.error("[ERROR] [%s] in backup %s" % (now_datetime, r[0]))

                    self.drop_dir_datetime(now_datetime, ruta_backup)

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
                name_split = s["name"].split("---")
                try:
                    name_date = name_split[1]
                except Exception as e:
                    key = False
                    print e
                    logging.error(e)

                if datetime.strptime(name_date, "%Y-%m-%d").strftime("%Y-%m-%d") <= drop_datetime.strftime("%Y-%m-%d"):
                    logging.warning("[INFO] [%s] Drop snapshot %s" % (now_datetime, s["name"]))
                    print "[INFO] [%s] Drop snapshot %s" % (now_datetime, s["name"])
                    self.gtools.delete_snapshot(self.dic_argv["project"],s["name"])
        else:
            print "[INFO] Not found snapshot that are on or out the erase date: %s" % drop_datetime

    def start_kube_backup(self):
        now_datetime = datetime.now()
        list_db = self.get_configmap(self.name_configmap_backup, self.dic_argv["conf_mode"])
        for db in list_db:
            #print db
            self.bakup_sql(db, now_datetime)

    def snapshot(self):
        self.gtools = gcloud_tools()
        now_datetime = datetime.now()
        list_disk = self.get_configmap(self.name_configmap_snapshot, self.dic_argv["conf_mode"])
        
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
    if dic_argv.get("mode", False) == "backup":
        if kluster.check(kluster.name_configmap_backup, dic_argv["conf_mode"]):
            kluster.start_kube_backup()

    elif dic_argv.get("mode", False) == "snapshot":
        if kluster.check(kluster.name_configmap_snapshot, dic_argv["conf_mode"]):
            kluster.snapshot()
    else:
        print "[ERROR] Mode not found"


if __name__ == '__main__':
    # Start
    main()
