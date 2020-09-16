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

class get_methods:

    system('echo "Init get_methods..."')
    
    def get_ip_from_service(self, name, services, namespace = "", ip_error=environ['IP_ERROR']):
        #services = self.v1.list_service_for_all_namespaces(watch=False)
        list_svc = []
        for s in services.items:
            if namespace == "":
                if s.metadata.name == name:
                    try:
                        return s.spec.cluster_ip
                    except:
                        return ip_error
            else:
                if s.metadata.name == name and s.metadata.namespace == namespace:
                    # system('echo "[INFO] %s - %s: %s"' % (name, namespace, s.spec.cluster_ip))
                    try:
                        return s.spec.cluster_ip
                    except:
                        return ip_error

    def get_selector_from_service(self, name, services, namespace = ""):
        #services = self.v1.list_service_for_all_namespaces(watch=False)
        list_svc = []
        for s in services.items:
            if s.metadata.name == name and s.metadata.namespace == namespace:
                try:
                    return s.spec.selector
                except:
                    return {'not-found': 'true'}

    def get_ip_from_pod(self, svc_labels, namespace, pods, ip_error=environ['IP_ERROR']):
        #pod = self.v1.list_pod_for_all_namespaces(watch=False)
        # Only for pods
        list_ip_pod = []
        for p in pods.items:
            if p.metadata.namespace == namespace:
                key_search = None
                if svc_labels == p.metadata.labels:
                    key_search = True
                else:
                    for key in svc_labels.keys():
                        if svc_labels.get(key, 'False_dic1') == p.metadata.labels.get(key, 'False_dic2') \
                          and (key_search or key_search == None):
                            key_search = True
                        else:
                            key_search = False
                if key_search:
                    list_ip_pod.append(p.status.pod_ip)
        if list_ip_pod == []:
            list_ip_pod.append(ip_error)
        return list_ip_pod

    def get_ip_from_deployment(self, name, namespace, pods, replica_sets, ip_error=environ['IP_ERROR']):
        #replica_set = self.extv1beta1.list_replica_set_for_all_namespaces(watch=False)
        owner_replicaset = None
        for rs in replica_set.items:
            if rs.metadata.owner_references[0].kind == "Deployment"\
                    and rs.metadata.owner_references[0].name == name\
                    and rs.metadata.namespace == namespace\
                    and rs.spec.replicas > 0:
                owner_replicaset = rs.metadata.name
                self.level_print('debug', owner_replicaset)

        list_ip = []
        #pods = self.v1.list_pod_for_all_namespaces(watch=False)
        not_found_pod = True
        for p in pods.items:
            if p.metadata.owner_references:
                #exec("annotation_pod = " + str(p.metadata.annotations.get("kubernetes.io/created-by", {})))
                annotation_pod = p.metadata.owner_references[0]
                #self.level_print('debug' , 'echo "%s"' % (annotation_pod))
                #annotation_pod = annotation_pod.get("reference", {})
                #self.level_print('debug', annotation_pod)
                if annotation_pod != {}:
                    if annotation_pod.kind == "ReplicaSet"\
                            and annotation_pod.name == owner_replicaset\
                            and p.metadata.namespace == namespace:
                        not_found_pod = False
                        try:
                            if p:
                                list_ip.append(p.status.pod_ip)
                        except:
                            list_ip.append(ip_error)
        if not_found_pod:
            list_ip.append(ip_error)
        return list_ip

    def get_secret(self, ing_name_secret, ing_namespace_secret, secrets):
        #secrets = self.v1.list_secret_for_all_namespaces(watch=False)
        dic_cert = {}
        for s in secrets.items:
            if s.metadata.namespace == ing_namespace_secret and s.metadata.name == ing_name_secret:
                system('echo "[INFO] Get secret ingress %s"' % (s.metadata.name))

                dir_name = s.metadata.namespace + '_' + s.metadata.name
                system("rm -rf %s/certs/%s; mkdir %s/certs/%s" % (self.ruta_exec, dir_name, self.ruta_exec, dir_name))
                for d in s.data:
                    patch_cert = '%s/certs/%s/%s' % (self.ruta_exec, dir_name, str(d))
                    # list_certs.append({str(d): patch_cert})
                    dic_cert[str(d)] = str(patch_cert)
                    system("echo '%s' > %s" % (b64decode(s.data[d]), patch_cert))
        return dic_cert

    def dic_get_secret_namespaced(self, ing_name_secret, ing_namespace_secret, secrets):
        dic_cert = {}
        system('echo "[INFO](dic_get_secret_namespaced) %s %s"' % (ing_name_secret, ing_namespace_secret))
        if ing_name_secret != environ['DEFAULT_CERT'] \
          or ing_namespace_secret != environ['DEFAULT_CERT_NAMESPACE']:
            #secrets = self.v1.list_namespaced_secret(ing_namespace_secret, watch=False)
            for s in secrets.items:
                if s.metadata.namespace == ing_namespace_secret and s.metadata.name == ing_name_secret:
                    system('echo "[INFO] Found secret namespaced for ingress %s"' % (s.metadata.name))
                    dir_name = s.metadata.namespace + '_' + s.metadata.name
                    for d in s.data:
                        patch_cert = '%s/certs/%s/%s' % (self.ruta_exec, dir_name, str(d))
                        dic_cert[str(d)] = str(patch_cert)
        if dic_cert == {}:
            dic_cert['tls.crt'] = '/files/liberty-ingress/certs/kube-system_liberty-tls/tls.crt'
            dic_cert['tls.key'] = '/files/liberty-ingress/certs/kube-system_liberty-tls/tls.key'
        return dic_cert

    def proc_path(self, b):
        if b.path == "/":
            backend_path = ""
        else:
            backend_path = b.path
        if backend_path is None:
            backend_path = ""
        return backend_path

    def get_hosts(self, i, pods, services, replica_sets, ip_error=environ['IP_ERROR'], port_error=environ['PORT_ERROR']):
        list_hosts = []
        client_ssl = "False"
        for host in i.spec.rules:
            #print host
            list_backend = []
            if i.metadata.annotations.get('ingress-liberty/backend-entity', False) == 'deployment':
                type_backend = "deployment"
                for b in host.http.paths:
                    svc_ip_list = self.get_ip_from_deployment(b.backend.service_name, i.metadata.namespace, pods, replica_sets, ip_error)
                    svc_port = b.backend.service_port
                    backend_path = self.proc_path(b)
                    for svc_ip in svc_ip_list:
                        if svc_ip == None or svc_ip == ip_error:
                            svc_ip = ip_error
                            svc_port = port_error
                        list_backend.append({'service_ip': svc_ip, 'service_port': svc_port, 'backend-entity': 'deployment', 
                            'backend_name': backend_path.replace("/", ""), 'backend_path': backend_path})
            else:
                type_backend = "all"
                for b in host.http.paths:
                    if i.metadata.annotations.get('ingress-liberty/backend-entity', False) == 'service':
                        svc_ip = self.get_ip_from_service(b.backend.service_name, services, i.metadata.namespace, ip_error)
                        svc_port = b.backend.service_port
                        backend_path = self.proc_path(b)
                        #system('echo "IP ' + b.backend.service_name + ': ' + str(svc_ip) + '"')
                        if svc_ip == None or svc_ip == ip_error:
                            svc_ip = ip_error
                            svc_port = port_error
                        list_backend.append({'service_ip': svc_ip, 'service_port': svc_port, 
                            'backend_name': backend_path.replace("/", ""), 'backend_path': backend_path})
                    else:
                        #svc_ip = self.get_ip_from_pod(b.backend.service_name, i.metadata.namespace, pods, ip_error)
                        svc_labels = self.get_selector_from_service(b.backend.service_name, services, i.metadata.namespace)
                        svc_ip_list = self.get_ip_from_pod(svc_labels, i.metadata.namespace, pods, ip_error)
                        svc_port = b.backend.service_port
                        backend_path = self.proc_path(b)
                        for svc_ip in svc_ip_list:
                            if svc_ip == None or svc_ip == ip_error:
                                svc_ip = ip_error
                                svc_port = port_error
                            list_backend.append({'service_ip': svc_ip, 'service_port': svc_port, 'backend-entity': 'pod', 
                                'backend_name': backend_path.replace("/", ""), 'backend_path': backend_path})
            if i.metadata.annotations.get('ingress-liberty/ssl-client', False) == "True":
                client_ssl = "True"
            list_hosts.append(
                {'host_name': host.host, 'name_upstream': host.host.replace(".", "-"), 'type_backend':type_backend,\
                 'backends': list_backend, 'client_ssl': client_ssl, 'timeout': environ['TIMEOUT']})
        return list_hosts

    def get_ingress(self):
        system('echo "[INFO] Class for Liberty: %s"' % environ['NAME_LIBERTY'])
        secrets = self.v1.list_secret_for_all_namespaces(watch=False)
        self.get_secret("liberty-tls", "kube-system", secrets)
        old_list_ing = [2]
        while True:
            system('echo "\033[1m[INFO]\033[00m Verifying the changes in Kubernetes"')
            found_tls_acme = False
            list_ing = []
            try:
                ing = self.extv1beta1.list_ingress_for_all_namespaces(watch=False)
                secrets = self.v1.list_secret_for_all_namespaces(watch=False)
                pods = self.v1.list_pod_for_all_namespaces(watch=False)
                services = self.v1.list_service_for_all_namespaces(watch=False)
                try:
                    replica_sets = self.extv1beta1.list_replica_set_for_all_namespaces(watch=False)
                except:
                    replica_sets = self.appsv1.list_replica_set_for_all_namespaces(watch=False)
                for i in ing.items:
                    if i.metadata.annotations:
                        if i.metadata.annotations.get('kubernetes.io/ingress.class', False) == environ['NAME_LIBERTY']:
                            # system('echo "[INFO] Found mode in ingress %s"' % (i.metadata.name))

                            # Modos
                            #found_tls_acme = False
                            if i.metadata.annotations.get('ingress-liberty/mode', False) == 'ssl':
                                system('echo "[INFO] Mode SSL ingress %s"' % (i.metadata.name))
                                list_hosts = self.get_hosts(i, pods, services, replica_sets)

                                if i.metadata.annotations.get('ingress-liberty/backend', False):
                                    backend = i.metadata.annotations.get('ingress-liberty/backend', False)

                                if i.metadata.annotations.get('ingress-liberty/ssl-secret', False) \
                                        and i.metadata.annotations.get('ingress-liberty/ssl-namespace', False):

                                    ing_name_secret = i.metadata.annotations.get('ingress-liberty/ssl-secret', False)
                                    ing_namespace_secret = i.metadata.annotations.get('ingress-liberty/ssl-namespace', False)

                                    list_certs = self.dic_get_secret_namespaced(ing_name_secret, ing_namespace_secret, secrets)

                                else:
                                    system('echo "[WARNING] Not found cert SSL in ingress %s"' % (i.metadata.name))

                                dic_ing = {'name_ing': i.metadata.name, 'ing_namespace_secret': ing_namespace_secret,
                                           'ing_name_secret': ing_name_secret, 'list_hosts': list_hosts, 'mode': 'ssl',
                                           'dic_certs': list_certs, 'backend': backend, 'patch': self.ruta_exec}
                                list_ing.append(dic_ing)

                            elif i.metadata.annotations.get('ingress-liberty/mode', False) == 'tcp':
                                system('echo "[INFO] Mode TCP ingress %s"' % (i.metadata.name))
                                list_hosts = self.get_hosts(i, pods, services, replica_sets)
                                port = i.metadata.annotations.get('ingress-liberty/tcp-port', False)
                                dic_ing = {'name_ing': i.metadata.name, 'list_hosts': list_hosts, 'mode': 'tcp', 'port': port,
                                           'patch': self.ruta_exec}
                                list_ing.append(dic_ing)

                            elif i.metadata.annotations.get('ingress-liberty/mode', False) == 'tls-acme' \
                                and i.metadata.annotations.get('kubernetes.io/tls-acme', False) == 'true':

                                system('echo "[INFO] Mode TLS-ACME ingress %s"' % (i.metadata.name))
                                found_tls_acme = True
                                list_hosts = self.get_hosts(i, pods, services, replica_sets)

                                if i.metadata.annotations.get('ingress-liberty/backend', False):
                                    backend = i.metadata.annotations.get('ingress-liberty/backend', False)

                                list_certs=[]
                                for secret in i.spec.tls:
                                    dic_certs={}
                                    dic_certs[secret.secret_name] = self.dic_get_secret_namespaced(secret.secret_name, i.metadata.namespace, secrets)
                                    dic_certs["secret_name"] = secret.secret_name
                                    dic_certs["hosts"] = secret.hosts
                                    list_certs.append(dic_certs)

                                dic_ing = {'name_ing': i.metadata.name, 'ing_namespace_secret': i.metadata.namespace,
                                           'list_hosts': list_hosts, 'mode': 'tls-acme',
                                           'dic_certs': list_certs, 'backend': backend, 'patch': self.ruta_exec,
                                           'name_cert_generator': environ['SVC_CERT_GENERATOR'], 'namespace_cert_generator': environ['NAMESPACE_CERT_GENERATOR']}
                                list_ing.append(dic_ing)

                freeze_list_ing = list(list_ing)
                ddiff = DeepDiff(freeze_list_ing, old_list_ing)
                if ddiff:
                    system('echo "[INFO] Diff: %s"' % ddiff)
                    # Search cert_generator
                    if found_tls_acme:
                        name_cert_generator = environ['SVC_CERT_GENERATOR']
                        port_cert_generator = environ['SVC_CERT_GENERATOR_PORT']
                        ip_cert_generator = self.get_ip_from_service(name_cert_generator, services)
                        list_hosts = [{"name_upstream": name_cert_generator, "backend": {"service_ip": ip_cert_generator, \
                            "service_port": port_cert_generator}}]
                        dic_cert_generator = { "mode": "cert_generator", "list_hosts" : list_hosts}
                        list_ing.append(dic_cert_generator)
                    system('echo "%s"' % freeze_list_ing)
                    #pprint.PrettyPrinter(indent=4).pprint(list_ing)
                    for i in list_ing:
                        if i['mode'] == 'ssl':
                            system('echo "[DEBUG] Configure mode ssl"')
                            #system('echo "%s"' % i)
                            dic_cert = self.get_secret(i["ing_name_secret"], i["ing_namespace_secret"],secrets)
                            if dic_cert == {}:
                                list_ing.remove(i)
                                system('echo "[ERROR] Not Found %s in namespace %s"' % (i["ing_name_secret"], i["ing_namespace_secret"]))
                                sleep(5)
                        elif i['mode'] == 'tls-acme':
                            system('echo "[DEBUG] Configure mode tls-acme"')
                            for secret in i["dic_certs"]:
                                dic_cert = self.get_secret(secret["secret_name"], i["ing_namespace_secret"], secrets)
                    system('echo "\033[1m[RELOAD-WRITE]\033[00m Write conf nginx"')
                    self.write_conf(list_ing, 'nginx-template', '/etc/nginx/sites-enabled/default')
                    self.write_conf(list_ing, 'nginx-template-tcp', '/etc/nginx/others/default')
                    if not path.exists('/.dockerenv'):
                        break
                    self.reload()
                else:
                    system('echo "\033[1m[INFO]\033[00m Diff without differences"')

                # print list_ing
                old_list_ing = freeze_list_ing
                sleep(int(self.dic_argv["time_query"]))

            except Exception as e:
                system('echo "[ERROR] %s %s"' % (e.message, e.args))
                traceback.print_exc()
                sleep(5)

    def get_svc(self, services):
        for i in services.items:
            try:
                pass
            # {i.spec.cluster_ip, i.metadata.namespace, i.metadata.name, i.metadata.labels['ssl-balance'], i.metadata.labels['domain']}
            except Exception as e:
                # print e
                pass