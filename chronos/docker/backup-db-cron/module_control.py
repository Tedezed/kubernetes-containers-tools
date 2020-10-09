#!/usr/bin/python3
# -*- coding: utf-8 -*-

# By: Juan Manuel Torres (Tedezed)
# Source: https://github.com/Tedezed
# Mail: juanmanuel.torres@aventurabinaria.es

import psycopg2, base64, sys, os, ast, importlib, logging

from passlib.hash import pbkdf2_sha512
from sendmail import *

class main_module():

    def __init__(self,
                chronos,
                input_mode,
                input_conf,
                input_now_datetime,
                input_chronos_logging,
                input_debug=False):

        self.chronos = chronos
        self.mode = input_mode
        self.conf_list = input_conf
        self.now_datetime = input_now_datetime
        self.chronos_logging = input_chronos_logging
        self.debug_mode = input_debug

        # Get list of modules
        self.manifestname = '__manifest__.py'
        self.current_path = os.path.dirname(os.path.abspath(__file__))
        self.name_dir_modules = "modules"
        self.path_modules = "%s/%s/%s" % (self.current_path, self.name_dir_modules, self.mode)
        self.relative_path_modules = "%s/%s" % (self.name_dir_modules, self.mode)

        if os.path.isdir(self.path_modules):
            self.modules = []
            obj_modules = os.walk(self.path_modules)
            for mod in obj_modules:
                if mod[0] == self.path_modules:
                    print("[INFO] Mode: %s. Load Modules.." % self.mode)
                    self.modules = mod[1]
                    print("[INFO] Load: %s" % self.modules)
        else:
            raise Exception("[ERROR] Dir modules not found: %s " % self.path_modules)

    def load_manifest(self, mod):
        manifest_file = "%s/%s/%s" % (self.path_modules, mod, self.manifestname)
        if os.path.isfile(manifest_file):
            m = open(manifest_file,"rb")
            try:
                manifestmod = ast.literal_eval(m.read().decode('utf-8'))
            finally:
                m.close()
            return manifestmod
        else:
            return False
                
    def load_module(self, mod):
        mod_to_load = '%s.%s' % (self.relative_path_modules.replace("/", "."), mod)
        importmod = importlib.import_module(mod_to_load)
        return importmod.main.chronos_module(self)

    def conditional_module(self):
        for job in self.conf_list:
            module_for_job = False
            for mod in self.modules:
                manifestmod = self.load_manifest(mod)
                if manifestmod:
                    if manifestmod["executable"]:
                        print("[INFO] Check module '%s' is executable" % manifestmod["name"])
                        if job["type"] == manifestmod["type"]:
                            print(job)
                            print("[INFO] Execute module '%s' for %s" % (manifestmod["name"], job["name_svc"]))
                            # Load Module
                            self.input_job = job
                            try:
                                sm = self.load_module(mod)
                                if sm:
                                    path_backup = sm.chronos_job()
                                    module_for_job = True
                                    if self.mode == "databases":
                                        self.chronos.drop_dir_datetime(self.now_datetime, path_backup)
                                else:
                                    print("[ERROR] Impossible to load the module: %s" % manifestmod["name"])
                            except Exception as e:
                                error = '[ERROR] [%s] host %s not found ' % (self.now_datetime , job["name_svc"])
                                if self.debug_mode:
                                    print("host: %s, user: %s, pass: %s, port: %s" \
                                      % (job["host"], \
                                         job["database_username"], \
                                         job["database_password"], \
                                         job["port"]))
                                print(error, e)
                                self.chronos_logging.error(error, e)
                                send_mail("[ERROR BACKUP] %s" % (job["name_svc"]), error, self.debug_mode)
            manifestmod = False
            if not module_for_job:
                error = '[WARNING] Not module for job %s, type: %s' % (job["name_svc"], job["type"])
                print(error)
                self.chronos_logging.error(error)
                send_mail("[ERROR BACKUP] %s %s" % (job["name_svc"], job["host"]), error, self.debug_mode)
