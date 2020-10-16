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
                input_now_datetime,
                input_chronos_logging,
                input_debug=False):

        self.chronos = chronos
        self.mode = input_mode
        self.now_datetime = input_now_datetime
        self.chronos_logging = input_chronos_logging
        self.debug_mode = input_debug

        # Get list of modules
        self.manifestname = '__manifest__.py'
        self.current_path = os.path.dirname(os.path.abspath(__file__))
        self.name_dir_modules = "modules"
        self.path_modules = "%s/%s" % (self.current_path, self.name_dir_modules)
        self.relative_path_modules = "%s/" % (self.name_dir_modules)

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
        #mod_to_load = '%s.%s' % (self.relative_path_modules.replace("/", "."), mod)
        mod_to_load = '%s%s' % (self.relative_path_modules.replace("/", "."), mod)
        print("[INFO] Mod to load: %s" % mod_to_load)
        importmod = importlib.import_module(mod_to_load)
        return importmod.main.chronos_module(self)

    """
    Bare Modules
        This type of module will be invoked only by "chronos_complex_job" with a list containing all the jobs if 
        conf_mode=="configmap" is used or nothing in the case of using conf_mode: "API", in the latter case it will
        have to be able to make requests to obtain the list of jobs.
        Designed for maximum customization which makes them more complex.
    """
    def exec_bare_modules(self, conf_list):
        print("[INFO] (exec_bare_modules)")
        for mod in self.modules:
            manifestmod = self.load_manifest(mod)
            if manifestmod:
                if manifestmod["executable"] and manifestmod["mode"] == self.mode:
                    print("[INFO] Check module '%s' is executable" % manifestmod["name"])
                    try:
                        sm = self.load_module(mod)
                        if sm:
                            sm.chronos_complex_job(conf_list)
                        else:
                            print("[ERROR] Impossible to load the module: %s" % manifestmod["name"])
                    except Exception as e:
                        error = '[ERROR] (module_custom_list_job) mode: %s' % self.mode
                        print(error, e)
                        self.chronos_logging.error(error, e)
                        send_mail("[ERROR BACKUP] %s" % ("(module_custom_list_job)"), error, self.debug_mode)

    """
    Methodical Modules
        This type of module will be called for each job with "chronos_job".
        It allows to create modules in a simple and fast way.
    """
    def exec_methodical_modules(self, conf_list):
        print("[INFO] (exec_methodical_modules)")
        for job in conf_list:
            module_for_job = False
            for mod in self.modules:

                manifestmod = self.load_manifest(mod)
                if manifestmod:
                    if manifestmod["executable"] and manifestmod["mode"] == self.mode:
                        print("[INFO] Check module '%s' is executable" % manifestmod["name"])
                        print(job)
                        if job["job_type"] == manifestmod["job_type"]:
                            print(job)
                            print("[INFO] Execute module '%s' for %s" % (manifestmod["name"], job["job_name"]))

                            # Load Module
                            self.input_job = job
                            try:
                                sm = self.load_module(mod)
                                if sm:
                                    output_job = sm.chronos_job()
                                    module_for_job = True
                                    if self.mode == "methodical_modules":
                                        self.chronos.drop_dir_datetime(self.now_datetime, output_job)
                                else:
                                    print("[ERROR] Impossible to load the module: %s" % manifestmod["name"])

                            except Exception as e:
                                error = '[ERROR] [%s] host %s not found ' % (self.now_datetime , job["job_name"])
                                print(error, e)
                                self.chronos_logging.error(error, e)
                                send_mail("[ERROR BACKUP] %s" % (job["job_name"]), error, self.debug_mode)

            manifestmod = False
            if not module_for_job:
                error = '[WARNING] Not module for job %s, type: %s' % (job["job_name"], job["job_type"])
                print(error)
                self.chronos_logging.error(error)
                send_mail("[ERROR BACKUP] %s " % error, error, self.debug_mode)
