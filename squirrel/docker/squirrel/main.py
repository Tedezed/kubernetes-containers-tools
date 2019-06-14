# password rotation (Squirrel, Nuts Warehouse)
# By Tedezed

import gnupg, random, string, re, json
from kubernetes import client, config
from os import path, getlogin, system, getuid, environ
from sys import argv

from controller.controller import *
from cronjob.cronjob import *

class sqrl():

    # Basic
    ruta_exec = path.dirname(path.realpath(__file__))
    squirrel_away = "%s/away" % ruta_exec
    squirrel_controller = "%s/controller" % ruta_exec
    len_password = 22
    nut_list = []
    nuts = {}

    # Controller
    domain_api = "squirrel.local"

    # GPG
    try:
        gpg = gnupg.GPG(gnupghome=squirrel_away) 
    except TypeError:
        gpg = gnupg.GPG(homedir=squirrel_away)

    def __init__(self):

        def argument_to_dic(list):
            dic = {}
            for z in list:
                dic[z[0]] = z[1]
            return dic

        def log_terminal(level, text):
            format_log = "[%s] %s"
            if level == 0:
                return format_log % ("DEBUG", text)
            elif level == 1:
                return format_log % ("INFO", text)
            elif level == 2:
                return format_log % ("ERROR", text)

        # Read arguments
        list_argv = []
        argv.remove(argv[0])
        for elements in argv:
            variable_entrada = elements.split("=")
            if len(variable_entrada) == 1 or variable_entrada[1] == '':
                raise NameError(log_terminal(2, 'Invalid Arguments [python example.py var="text"]'))
            list_argv.append(variable_entrada)
        self.dic_argv = argument_to_dic(list_argv)

        # Load Kubernetes Config
        if not path.exists('/.dockerenv'):
            try:
                config.load_kube_config()
            except OSError:
                config.load_kube_config(config_file='/home/%s/.kube/config-slug' % (pwd.getpwuid(getuid()).pw_name))
        else:
            config.load_incluster_config()

        # Define Kubernetes API
        self.v1 = client.CoreV1Api()
        self.extv1beta1 = client.ExtensionsV1beta1Api()

def main():
    squirrel = sqrl()
    if squirrel.dic_argv.get("mode", False) == "controller":
        controller.daemon_controller(squirrel)
    elif squirrel.dic_argv.get("mode", False) == "cronjob":
        cronjob.daemon_controller(squirrel)
    else:
        print("Use: mode=(controller or cronjob)")

if __name__ == '__main__':
    # Start
    main()