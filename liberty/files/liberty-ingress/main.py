#!/usr/bin/python
# -*- coding: utf-8 -*-

# Ingress Controller Liberty

# Source: https://github.com/Tedezed
# Mail: juanmanuel.torres@aventurabinaria.es

from kubernetes import client, config
import pwd
from os import path, getlogin, system, getuid
from sys import argv
from base64 import b64decode
from deepdiff import DeepDiff
from jinja2 import Environment, FileSystemLoader
from time import sleep


class kube_init:
    ruta_exec = path.dirname(path.realpath(__file__))
    v1 = None
    extv1beta1 = None
    bash_bold = '\033[1m'
    bash_none = '\033[00m'

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
                config.load_kube_config(config_file='/home/%s/.kube/slug-config-2' % (getlogin()))
            except OSError:
                config.load_kube_config(config_file='/home/%s/.kube/slug-config-2' % (pwd.getpwuid(getuid()).pw_name))
        # config.load_kube_config()
        # config.load_kube_config(config_file='%s/credentials/config' % (self.ruta_exec))
        else:
            config.load_incluster_config()

        # Define API
        self.v1 = client.CoreV1Api()
        self.extv1beta1 = client.ExtensionsV1beta1Api()

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

    def reload(self):
        system('chown www-data:www-data %s/certs/*' % (self.ruta_exec))
        system('chown www-data:www-data -R /etc/nginx/*')
        system('nginx -t')
        system('service nginx reload')

    def get_ip_from_service(self, name, namespace):
        services = self.v1.list_service_for_all_namespaces(watch=False)
        list_svc = []
        for s in services.items:
            if s.metadata.name == name and s.metadata.namespace == namespace:
                # system('echo "[INFO] %s - %s: %s"' % (name, namespace, s.spec.cluster_ip))
                try:
                    return s.spec.cluster_ip
                except:
                    return "169.254.10.90"

    def get_ip_from_pod(self, name, namespace):
        pod = self.v1.list_pod_for_all_namespaces(watch=False)
        for p in pod.items:
            if p.metadata.name == name and p.metadata.namespace == namespace:
                try:
                    return p.status.pod_ip
                except:
                    return "169.254.10.90"

    def get_secret(self, ing_name_secret, ing_namespace_secret):
        secrets = self.v1.list_secret_for_all_namespaces(watch=False)
        for s in secrets.items:
            if s.metadata.namespace == ing_namespace_secret and s.metadata.name == ing_name_secret:
                system('echo "[INFO] Get secret ingress %s"' % (s.metadata.name))

                dir_name = s.metadata.namespace + '_' + s.metadata.name
                system("rm -rf %s/certs/%s; mkdir %s/certs/%s" % (self.ruta_exec, dir_name, self.ruta_exec, dir_name))
                dic_cert = {}
                for d in s.data:
                    patch_cert = '%s/certs/%s/%s' % (self.ruta_exec, dir_name, str(d))
                    # list_certs.append({str(d): patch_cert})
                    dic_cert[str(d)] = str(patch_cert)
                    system("echo '%s' > %s" % (b64decode(s.data[d]), patch_cert))
        return dic_cert

    def dic_get_secret(self, ing_name_secret, ing_namespace_secret):
        secrets = self.v1.list_secret_for_all_namespaces(watch=False)
        for s in secrets.items:
            if s.metadata.namespace == ing_namespace_secret and s.metadata.name == ing_name_secret:
                # system('echo "[INFO] Found secret for ingress %s"' % (s.metadata.name))

                dir_name = s.metadata.namespace + '_' + s.metadata.name
                dic_cert = {}
                for d in s.data:
                    patch_cert = '%s/certs/%s/%s' % (self.ruta_exec, dir_name, str(d))
                    dic_cert[str(d)] = str(patch_cert)
        return dic_cert

    def get_hosts(self, i):
        list_hosts = []
        for host in i.spec.rules:
            list_backend = []
            for b in host.http.paths:
                if i.metadata.annotations.get('ingress-liberty/backend-entity', False) == 'pod':
                    svc_ip = self.get_ip_from_pod(b.backend.service_name, i.metadata.namespace)
                else:
                    svc_ip = self.get_ip_from_service(b.backend.service_name, i.metadata.namespace)
                svc_port = b.backend.service_port
                list_backend.append({'service_ip': svc_ip, 'service_port': svc_port})
            list_hosts.append(
                {'host_name': host.host, 'name_upstream': host.host.replace(".", "-"), 'backends': list_backend})
        return list_hosts

    def get_ingress(self):
        self.get_secret("liberty-tls", "kube-system")
        old_list_ing = [2]
        while True:
            try:
                ing = self.extv1beta1.list_ingress_for_all_namespaces(watch=False)
                list_ing = []
                for i in ing.items:
                    if i.metadata.annotations.get('kubernetes.io/ingress.class', False) == 'liberty':
                        # system('echo "[INFO] Found mode in ingress %s"' % (i.metadata.name))

                        # Modos
                        if i.metadata.annotations.get('ingress-liberty/mode', False) == 'ssl':

                            list_hosts = self.get_hosts(i)

                            if i.metadata.annotations.get('ingress-liberty/backend', False):
                                backend = i.metadata.annotations.get('ingress-liberty/backend', False)

                            if i.metadata.annotations.get('ingress-liberty/ssl-secret', False) \
                                    and i.metadata.annotations.get('ingress-liberty/ssl-namespace', False):

                                ing_name_secret = i.metadata.annotations.get('ingress-liberty/ssl-secret', False)
                                ing_namespace_secret = i.metadata.annotations.get('ingress-liberty/ssl-namespace', False)

                                list_certs = self.dic_get_secret(ing_name_secret, ing_namespace_secret)

                            else:
                                system('echo "[WARNING] Not found cert SSL in ingress %s"' % (i.metadata.name))

                            dic_ing = {'name_ing': i.metadata.name, 'ing_namespace_secret': ing_namespace_secret,
                                       'ing_name_secret': ing_name_secret, 'list_hosts': list_hosts, 'mode': 'ssl',
                                       'dic_certs': list_certs, 'backend': backend, 'patch': self.ruta_exec}
                            list_ing.append(dic_ing)

                        elif i.metadata.annotations.get('ingress-liberty/mode', False) == 'tcp':
                            list_hosts = self.get_hosts(i)
                            port = i.metadata.annotations.get('ingress-liberty/tcp-port', False)
                            dic_ing = {'name_ing': i.metadata.name, 'list_hosts': list_hosts, 'mode': 'tcp', 'port': port,
                                       'patch': self.ruta_exec}
                            list_ing.append(dic_ing)

                ddiff = DeepDiff(list_ing, old_list_ing)
                if ddiff:
                    for i in list_ing:
                        if i['mode'] == 'ssl':
                            self.get_secret(i["ing_name_secret"], i["ing_namespace_secret"])
                    system('echo "\033[1m[RELOAD-WRITE]\033[00m Write conf nginx"')
                    print list_ing
                    self.write_conf(list_ing, 'nginx-template', '/etc/nginx/sites-enabled/default')
                    self.write_conf(list_ing, 'nginx-template-tcp', '/etc/nginx/others/default')
                    self.reload()

                # print list_ing
                old_list_ing = list_ing
                sleep(int(self.dic_argv["time_query"]))

            except Exception as e:
                print e.message, e.args
                sleep(20)
                pass


    def get_svc(self):
        ret = self.v1.list_service_for_all_namespaces(watch=False)
        for i in ret.items:
            try:
                pass
            # {i.spec.cluster_ip, i.metadata.namespace, i.metadata.name, i.metadata.labels['ssl-balance'], i.metadata.labels['domain']}
            except Exception as e:
                # print e
                pass


def main():
    kluster = kube_init()
    kluster.get_ingress()


if __name__ == '__main__':
    # Start
    main()
