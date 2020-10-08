#!/usr/bin/python3
# -*- coding: utf-8 -*-

# By: Juan Manuel Torres (Tedezed)
# Source: https://github.com/Tedezed
# Mail: juanmanuel.torres@aventurabinaria.es

import mysql.connector, subprocess
from os import path, getlogin, system, listdir, getuid, environ

class chronos_module():

    def __init__(self, chronos):
        self.chronos = chronos
        self.loggin = self.chronos.chronos_logging
        self.job = self.chronos.input_job
        self.svc = self.job["name_svc"]
        self.host = self.job["host"]
        self.port = self.job["port"]
        self.user = self.job["database_username"]
        self.passwd = self.job["database_password"]

    def chronos_job(self):
        print(self.job)
        conn = mysql.connect(dbname='postgres', \
                                  user=self.user, \
                                  host=self.host, \
                                  password=self.passwd, \
                                  port=self.port\
                                )
        self.loggin.info('[INFO] [%s] Connect to %s ' \
          % (self.chronos.now_datetime, self.job["name_svc"]))
        
        cur = conn.cursor()
        cur.execute("""SHOW DATABASES""")
        rows = cur.fetchall()
        for r in rows:
            if r[0] not in ["template", \
                            "template0", \
                            "template1", \
                            "information_schema", \
                            "mysql", \
                            "performance_schema"]:

                path_service = self.chronos.path_service(self.job["name_svc"])
                path_backup = self.chronos.path_backup(path_service, str(r[0]))

                dump_command = 'mysqldump -u %s -p%s -h %s -P %s --databases %s > %s/%s___%s___%s.dump' % \
                                (self.job["database_username"], str(self.job["database_password"].encode('utf-8')), \
                                 self.host, self.job["port"], str(r[0]), \
                                path_backup, str(r[0]), self.chronos.now_datetime.strftime("%Y-%m-%d"), self.chronos.id_generator())

                self.chronos.execute_command(dump_command)
        return path_backup