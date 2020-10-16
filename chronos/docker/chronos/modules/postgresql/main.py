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
        self.job = self.module_control.input_job
        self.svc = self.job["job_name"]
        self.host = self.job["host"]
        self.port = self.job["port"]
        self.user = self.job["database_username"]
        self.passwd = self.job["database_password"]

    def chronos_job(self):
        print(self.job)
        conn = psycopg2.connect(dbname='postgres', \
                                  user=self.user, \
                                  host=self.host, \
                                  password=self.passwd, \
                                  port=self.port\
                                )
        self.loggin.info('[INFO] [%s] Connect to %s ' \
          % (self.module_control.now_datetime, self.job["job_name"]))
        
        cur = conn.cursor()
        cur.execute("""SELECT datname FROM pg_database""")
        rows = cur.fetchall()
        for r in rows:
            if r[0] not in ["template", \
                            "template0", \
                            "template1", \
                            "information_schema", \
                            "postgres", \
                            "performance_schema"]:

                path_service = self.module_control.chronos.path_service(self.job["job_name"])
                path_backup = self.module_control.chronos.path_backup(path_service, str(r[0]))

                dump_command = "pg_dump -Fc --dbname=postgresql://%s:'%s'@%s:%s/%s > %s/%s___%s___%s.dump" % \
                                (self.job["database_username"], str(self.job["database_password"]), \
                                self.host, self.job["port"], str(r[0]), \
                                path_backup, str(r[0]), self.module_control.now_datetime.strftime("%Y-%m-%d"), \
                                self.module_control.chronos.id_generator())
                                
                if self.module_control.chronos.debug:
                  print(dump_command)

                self.module_control.chronos.execute_command(dump_command)
        return path_backup