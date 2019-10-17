#!/usr/bin/python
# -*- coding: utf-8 -*-

# Ingress Controller Liberty
# Creator: Juan Manuel Torres
# Source: https://github.com/Tedezed
# Mail: juanmanuel.torres@aventurabinaria.es

from kubernetes import client, config
import pwd, traceback, pprint
from os import path, getlogin, system, getuid, environ
from sys import argv
from base64 import b64decode
from deepdiff import DeepDiff
from jinja2 import Environment, FileSystemLoader
from time import sleep

from nginx_brainslug import *
from get_methods import *
from elk_brainslug import *

class kube_init(nginx_brainslug, get_methods, elk_brainslug):
    
    ruta_exec = path.dirname(path.realpath(__file__))
    v1 = None
    extv1beta1 = None
    bash_bold = '\033[1m'
    bash_none = '\033[00m'
    #ip_error = "169.254.1.10"
    ip_error = "127.0.0.1"

    system('nginx -v')

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

        # Load Config
        if not path.exists('/.dockerenv'):
            try:
                #config.load_kube_config()
                config.load_kube_config(config_file='/home/%s/.kube/config-slug' % (getlogin()))
            except OSError:
                config.load_kube_config(config_file='/home/%s/.kube/config-slug' % (pwd.getpwuid(getuid()).pw_name))
        # config.load_kube_config()
        # config.load_kube_config(config_file='%s/credentials/config' % (self.ruta_exec))
        else:
            config.load_incluster_config()

        # Define API
        self.v1 = client.CoreV1Api()
        self.extv1beta1 = client.ExtensionsV1beta1Api()

    def level_print(self, level="None", text="Empty"):
        if environ['MODE'] == level:
            print(text)

def main():
    if environ['ELK'] == 'true':
        kluster = kube_init()
        elkb = elk_brainslug(kluster)
        if environ['ELK_MODE'] == 'start':
            while True:
                elkb.start_ingress()
                sleep(int(environ['TIME_QUERY']))
        else:
            elkb.stop_ingress()
    else:
        kluster = kube_init()
        kluster.get_ingress()

if __name__ == '__main__':
    # Start
    main()
