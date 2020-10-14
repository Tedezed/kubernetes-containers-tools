#!/usr/bin/python3
# -*- coding: utf-8 -*-

# By: Juan Manuel Torres (Tedezed)
# Source: https://github.com/Tedezed
# Mail: juanmanuel.torres@aventurabinaria.es

import psycopg2, subprocess
from os import path, getlogin, system, listdir, getuid, environ

class chronos_module():

    def __init__(self, module_control):
        self.module_control = module_control
        self.loggin = self.module_control.chronos_logging
        # self.job = self.module_control.input_job
        # self.svc = self.job["name_svc"]
        # self.host = self.job["host"]
        # self.port = self.job["port"]
        # self.user = self.job["database_username"]
        # self.passwd = self.job["database_password"]

    def chronos_job(self):
        pass