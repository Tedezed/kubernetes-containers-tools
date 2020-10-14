#!/usr/bin/python3
# -*- coding: utf-8 -*-

# By: Juan Manuel Torres (Tedezed)
# Source: https://github.com/Tedezed
# Mail: juanmanuel.torres@aventurabinaria.es

import base64

class squirrel_integration():

    def __init__(self, kube_init):
        self.kube_init = kube_init
        self.secrets = self.kube_init.v1.list_secret_for_all_namespaces(watch=False)

    def get_secrets(self):
        list_db = []
        for s in self.secrets.items:
            if s.metadata.annotations:
                for a in s.metadata.annotations:
                    if a == "squirrel_backup" and s.metadata.annotations[a] == "true":
                        if s.metadata.annotations.get("squirrel_service", False) and \
                          s.metadata.annotations.get("squirrel_type_backend", False):
                            dic_db = {}
                            dic_db["namespace"] = s.metadata.namespace
                            
                            dic_db["name_svc"] = s.metadata.annotations.get("squirrel_service", False)
                            squirrel_type_backend = s.metadata.annotations.get("squirrel_type_backend", False)
                            dic_db["type"] = squirrel_type_backend

                            squirrel_user_key = s.metadata.annotations.get("squirrel_username_key", False)
                            squirrel_pass_key = s.metadata.annotations.get("squirrel_password_key", False)
                            squirrel_user = s.data.get(squirrel_user_key, False)
                            squirrel_pass = s.data.get(squirrel_pass_key, False)
                            squirrel_user = str(base64.b64decode(squirrel_user + '=' * (-len(squirrel_user) % 4)).decode())
                            squirrel_pass = str(base64.b64decode(squirrel_pass + '=' * (-len(squirrel_pass) % 4)).decode())
                            
                            dic_db["database_username"] = squirrel_user
                            dic_db["database_password"] = squirrel_pass
                            if squirrel_type_backend == "postgres":
                                dic_db["port"] = s.metadata.annotations.get("custom_database_port", "5432")
                            elif squirrel_type_backend == "mysql":
                                dic_db["port"] = s.metadata.annotations.get("custom_database_port", "3306")
                            else:
                                print("[ERROR] Unexpected error - backend type...")
                                raise

                            #print(squirrel_user, squirrel_pass, squirrel_service, squirrel_type_backend, namespace, custom_database_port)
                            list_db.append(dic_db)
        return list_db
