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

        self.gtools = gcloud_tools()

    def chronos_create_job_list(self):
        list_disk = self.gtools.list_disks(self.module_control.chronos.dic_argv["project"], \
                      self.module_control.chronos.dic_argv["zone"])
        if list_disk:
            for disk in list_disk:
                disk_labels = disk.get("labels", [])
                disk_label_backup = "false"
                for l in disk_labels:
                    # backup_label = "backup"
                    if l == self.module_control.chronos.backup_label:
                        disk_label_backup = disk_labels[l]
                if disk.get("status", False) == "READY" and disk_label_backup.lower() ==  "true":
                    dict_disk = { "job_name": disk["name"], \
                                  "job_type": "gcp", \
                                  "name_disk": disk["name"], \
                                  "zone": self.module_control.chronos.dic_argv["zone"]}
                    list_disk.append(dict_disk)
        else:
            print("[WARNING] List disk is None...")
            list_disk = []
        return list_disk
