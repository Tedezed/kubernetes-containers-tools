#!/usr/bin/python
# -*- coding: utf-8 -*-

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

class nginx_brainslug:

    system('echo "Init nginx_brainslug..."')

    def load_ing_template(self, list_ing, file_conf):
        print file_conf
        dir_templates = self.ruta_exec + '/templates/'
        if path.exists(dir_templates + file_conf):
            j2_env = Environment(loader=FileSystemLoader(dir_templates),
                                 trim_blocks=True)
            return j2_env.get_template(file_conf).render(
                list_ing=list_ing,
                stats=True
            )
        else:
            system('echo "[ERROR] Not Found file template -> %s%s"' % (dir_templates, file_conf))
            exit()

    def write_conf(self, list_ing, file_conf, file_exit):
        template_render = self.load_ing_template(list_ing, file_conf)
        file_conf_template = open(file_exit, 'w')
        file_conf_template.write(template_render)
        file_conf_template.close()
        return template_render

    def level_print(self, level="None", text="Empty"):
        if environ['MODE'] == level:
            print(text)

    def reload(self):
        system('chown www-data:www-data %s/certs/*' % (self.ruta_exec))
        system('chown www-data:www-data -R /etc/nginx/*')
        system('nginx -t')
        system('service nginx reload')