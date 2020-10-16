#!/usr/bin/python3
# -*- coding: utf-8 -*-

# By: Juan Manuel Torres (Tedezed)
# Source: https://github.com/Tedezed
# Mail: juanmanuel.torres@aventurabinaria.es

import subprocess, os, sys
from os import path, getlogin, system, listdir, getuid, environ

from .gcloud_tools import gcloud_tools

class chronos_module():

    def __init__(self, module_control):
        self.module_control = module_control
        self.loggin = self.module_control.chronos_logging

        self.now_datetime = self.module_control.now_datetime

        self.gtools = gcloud_tools()

    def chronos_complex_job(self, conf_list):
        # If not get config in configmap, get config with gtools
        if not conf_list:
            list_disk = self.gtools.list_disks(self.module_control.chronos.dic_argv["project"], \
                      self.module_control.chronos.dic_argv["zone"])

        # If not configmap and generate in gtools raise warning
        if list_disk:
            for idx, disk in enumerate(list_disk):
                disk_labels = disk.get("labels", [])
                disk_label_backup = "false"
                for l in disk_labels:
                    # backup_label = "backup"
                    if l == self.module_control.chronos.backup_label:
                        disk_label_backup = disk_labels[l]
                if disk.get("status", False) == "READY" and disk_label_backup.lower() ==  "true":
                    list_disk[idx]["job_name"] = disk["name"]
                    list_disk[idx]["job_type"] = "gcp"
                    list_disk[idx]["name_disk"] = disk["name"]
                    list_disk[idx]["zone"] = self.module_control.chronos.dic_argv["zone"]
        else:
            print("[WARNING] List disk is None...")
            list_disk = []

        self.create_snaphot(list_disk)
        self.drop_snapshots(list_disk)
    
    def create_snaphots(self, list_disk):
        print(self.job)
        for disk in list_disk:
            if len(disk["name_disk"]) > 45:
                name_snapshot = disk["name_disk"][0:45] + "---" + self.now_datetime.strftime("%Y-%m-%d")
            else:
                name_snapshot = disk["name_disk"] + "---" + self.now_datetime.strftime("%Y-%m-%d")

            self.loggin.warning("[INFO] [%s] Create snapshot %s" % (self.now_datetime, name_snapshot))
            print("[INFO] [%s] Create snapshot %s" % (self.now_datetime, name_snapshot))
            try:
                if not self.module_control.chronos.debug:
                    self.gtools.disk_to_snapshot(self.module_control.chronos.dic_argv["project"], \
                      disk["zone"], disk["name_disk"], name_snapshot)
            except Exception as e:
                print(e)
                self.loggin.error(e)

    def drop_snapshots(self):
        drop_datetime = self.now_datetime - timedelta(days=int(self.dic_argv["subtract_days"]))
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
                            logging.warning("[INFO] [%s] Drop snapshot %s" % (self.now_datetime, s["name"]))
                            print("[INFO] [%s] Drop snapshot %s" % (self.now_datetime, s["name"]))
                            if not self.module_control.chronos.debug:
                                self.gtools.delete_snapshot(self.dic_argv["project"],s["name"])
                except Exception as e:
                    key = False
                    print(e)
                    logging.error(e)
        else:
            print("[INFO] Not found snapshot that are on or out the erase date: %s" % drop_datetime)
