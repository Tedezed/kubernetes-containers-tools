#!/usr/bin/python3

# By Tedezed
# https://www.saltycrane.com/blog/2011/10/python-gnupg-gpg-example/
# https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/ApiextensionsV1beta1Api.md

import gnupg, random, string, re, json, base64, hashlib, copy, re, pyperclip, time
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from os import path, getlogin, system, getuid, environ
from sys import argv

#from .app_update_pass import *
from .control_module import *

class nuts_manager():

    def __init__(self, squirrel):
        self.squirrel = squirrel
        self.squirrel_length_random = 26
        if path.exists('/.dockerenv'):
            config.load_incluster_config()
            self.configuration = client.Configuration()
            self.configuration.assert_hostname = False
            self.api_instance = client.ApiextensionsApi(client.ApiClient(self.configuration))
            self.api_client = client.api_client.ApiClient(configuration=self.configuration)

            self.crds = client.CustomObjectsApi(self.api_client)

    def randomStringDigits(self, stringLength=6):
        lettersAndDigits = string.ascii_letters + string.digits
        return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))

    def createKey(self, keyfile, email, password, keylen=1024, keytype='RSA'):
        print("Be patient...")
        pass_str = str(password)
        input_data = self.squirrel.gpg.gen_key_input(
            key_type=keytype,
            key_length=keylen,
            name_email=email,
            passphrase=pass_str)
        key = self.squirrel.gpg.gen_key(input_data)
        print("Key: ", key)
        self.exportKey(keyfile, str(key.fingerprint), pass_str)

    def exportKey(self, keyfile, key, password=None):
        try:
            ascii_armored_public_keys = self.squirrel.gpg.export_keys(key)
            ascii_armored_private_keys = self.squirrel.gpg.export_keys(key, secret=True)
        except:
            ascii_armored_public_keys = self.squirrel.gpg.export_keys(key)
            ascii_armored_private_keys = self.squirrel.gpg.export_keys(key, passphrase=password, secret=True)
        with open("%s.pub" % keyfile, 'w') as f:
            f.write(ascii_armored_public_keys)
        with open("%s.key" % keyfile, 'w') as f:
            f.write(ascii_armored_private_keys)

    def importKey(self, keyfile, key_data=False):
        if keyfile:
            key_data = open(keyfile).read()
        #print(key_data)
        import_result = self.squirrel.gpg.import_keys(key_data)
        print("[INFO] Import result %s" % import_result.results)

    def encryptText(self, email, text_to_encrypt):
        encrypted_data = self.squirrel.gpg.encrypt(text_to_encrypt, email, always_trust=True)
        encrypted_string = str(encrypted_data)
        #print(encrypted_data)
        print('encryptText ok: ', encrypted_data.ok)
        print('encryptText status: ', encrypted_data.status)
        #print('encryptText stderr: ', encrypted_data.stderr)
        #print('encryptText unencrypted_string: ', text_to_encrypt)
        #print('encryptText encrypted_string: ', encrypted_string)
        return encrypted_string

    def dencryptText(self, password, encrypted_string, mode=False):
        if mode == "base64":
            #print("Mode input base64")
            #print(encrypted_string)
            #print(base64.b64decode(encrypted_string + '=' * (-len(encrypted_string) % 4)).decode())
            decrypted_data = self.squirrel.gpg.decrypt(\
                str(base64.b64decode(encrypted_string + '=' * (-len(encrypted_string) % 4)).decode()),\
                passphrase=password)
        else:
            decrypted_data = self.squirrel.gpg.decrypt(encrypted_string, passphrase=password)
        print('dencryptText ok: ', decrypted_data.ok)
        print('dencryptText status: ', decrypted_data.status)
        #print('dencryptText stderr: ', decrypted_data.stderr)
        #print('dencryptText decrypted string: ', decrypted_data.data)
        #
        #pyperclip.copy(decrypted_data.data.decode())
        #return "[INFO] Password copied to the clipboard"
        #
        return "Content of the Nut: %s" % decrypted_data.data.decode()

    def away(self):
        public_keys = self.squirrel.gpg.list_keys()
        #re.findall("[a-zA-Z0-9_.-]*@[a-zA-Z0-9_.-]*",gpg.list_keys()[0]["uids"][0])
        for key in self.squirrel.gpg.list_keys():
            for uid in key.get("uids", False):
                if uid:
                    email = re.findall("[a-zA-Z0-9_.-]*@[a-zA-Z0-9_.-]*", uid)
                    self.nut_list.append(self.encryptText(email, self.randomStringDigits(self.len_password)))
        #print(self.dencryptText('1234567890',self.nut_list[0]))
        self.nuts["nuts"] = self.nut_list
        with open('%s/nuts.json' % self.squirrel_away, 'w') as outfile:  
            json.dump(self.nuts, outfile)

    def clean_dict(self, input_dict):
        try:
            del input_dict["api_version"]
            del input_dict["metadata"]["resource_version"]
            del input_dict["metadata"]["creation_timestamp"]
            del input_dict["metadata"]["uid"]
            del input_dict["metadata"]["self_link"]
            input_dict["apiVersion"] = 'v1'
        except Exception as e:
            print("[ERROR] %s" % e)
        return input_dict

    def string_to_list_format(self, text):
        text = text.replace(" ", "")
        text = text.split(",")
        return text

    def delete_pods(self, text_delete_pods, namespace):
        pods = self.squirrel.v1.list_namespaced_pod(namespace)
        for p in pods.items:
            for d in self.string_to_list_format(text_delete_pods):
                if bool(re.search(d, p.metadata.name)):
                    try: 
                        api_response = self.squirrel.v1.delete_namespaced_pod(p.metadata.name, namespace)
                        print("[INFO] Delete pod %s" % p.metadata.name)
                    except ApiException as e:
                        print("Exception when calling CoreV1Api->delete_namespaced_pod: %s\n" % e)

    def check_pods(self, text_delete_pods, namespace):
        pods = self.squirrel.v1.list_namespaced_pod(namespace)
        list_delete_pods = self.string_to_list_format(text_delete_pods)
        check = 0
        for p in pods.items:
            for d in list_delete_pods:
                if bool(re.search(d, p.metadata.name)):
                    print("Check", d, p.metadata.name, bool(re.search(d, p.metadata.name)))
                    check += 1
        if len(list_delete_pods) == check:
            return True
        else:
            return False

    def clean_nuts(self, valid_id_rotation, mode):
        crds = client.CustomObjectsApi()
        nuts = crds.list_cluster_custom_object(self.squirrel.domain_api, self.squirrel.api_version, 'nuts')["items"]
        nutcrackers = crds.list_cluster_custom_object(self.squirrel.domain_api, self.squirrel.api_version, 'nutcrackers')["items"]
        for n in nuts:

            # Nuts from nutcrackers that do not exist
            nut_nutcracker = n["data"].get("nutcracker", False)
            nut_nutcracker_found = False
            if mode == "old_nutcracker_clean":
                for nc in nutcrackers:
                    if nc["metadata"]["name"] == nut_nutcracker:
                        nut_nutcracker_found = True
            
            if (n["data"].get("id_rotation", 10000000000) != valid_id_rotation and mode == "id_clean") \
              or (not nut_nutcracker_found and mode == "old_nutcracker_clean"):
                try:
                    api_response = crds.delete_namespaced_custom_object(\
                        self.squirrel.domain_api, \
                        self.squirrel.api_version, \
                        n["metadata"]["namespace"], \
                        'nuts', \
                        n["metadata"]["name"],
                        client.V1DeleteOptions())
                    print(api_response)
                except ApiException as e:
                    print("Exception when calling CustomObjectsApi->delete_namespaced_custom_object: %s\n" % e)

    def rotation_secrets(self):
        secrets = self.squirrel.v1.list_secret_for_all_namespaces(watch=False)
        for s in secrets.items:
            if s.metadata.annotations:
                for a in s.metadata.annotations:
                    if a == "squirrel_rotation_secret" and s.metadata.annotations[a] == "true":
                        squirrel_length_random = s.metadata.annotations.get("squirrel_length_random", self.squirrel_length_random)
                        if s.metadata.annotations.get("squirrel_rotation_data", False):
                            s.kind = 'Secret'
                            secret = copy.deepcopy(s)
                            squirrel_rotation_data = self.string_to_list_format(s.metadata.annotations["squirrel_rotation_data"])
                            for d in squirrel_rotation_data:
                                new_pass = self.randomStringDigits(squirrel_length_random)
                                new_pass_base64 = base64.b64encode(new_pass.encode()).decode()
                                #new_pass_base64 = new_pass_base64 + '=' * (-len(new_pass_base64) % 4)
                                secret.data[d] = new_pass_base64
                            try:
                                if self.check_pods(s.metadata.annotations["squirrel_delete_pods"], secret.metadata.namespace):
                                    if not self.squirrel.debug:
                                        api_response = self.squirrel.v1.patch_namespaced_secret(secret.metadata.name, \
                                            secret.metadata.namespace, secret)
                                    print("(rotation_secrets)[INFO] Secret update with name %s and namespace %s" % (secret.metadata.name, secret.metadata.namespace))
                                    if s.metadata.annotations.get("squirrel_delete_pods", False):
                                        if s.metadata.annotations.get("squirrel_service", False) and \
                                          s.metadata.annotations.get("squirrel_type_frontend", False) and \
                                          s.metadata.annotations.get("squirrel_type_backend", False):
                                            squirrel_user_key = s.metadata.annotations.get("squirrel_username_key", False)
                                            squirrel_pass_key = s.metadata.annotations.get("squirrel_password_key", False)
                                            squirrel_user = s.data.get(squirrel_user_key, False)
                                            squirrel_pass = s.data.get(squirrel_pass_key, False)
                                            new_pass_decode = base64.b64decode(secret.data.get(\
                                                squirrel_pass_key, False) + '=' * (-len(secret.data.get(squirrel_pass_key, False)) % 4)).decode()
                                            aup = app_update_pass(s.metadata.annotations.get("squirrel_service", False),
                                                                  secret.metadata.namespace,
                                                                  squirrel_user,
                                                                  squirrel_pass,
                                                                  s.metadata.annotations.get("squirrel_type_frontend", False),
                                                                  s.metadata.annotations.get("squirrel_type_backend", False),
                                                                  s.metadata.annotations,
                                                                  "update_secret",
                                                                  new_pass_decode,
                                                                  self.squirrel.squirrel_nuts_manager,
                                                                  s,
                                                                  self.squirrel.debug)
                                            aup.conditional_app()
                                        if not self.squirrel.debug:
                                            self.delete_pods(s.metadata.annotations["squirrel_delete_pods"], secret.metadata.namespace)
                                            time.sleep(30)
                            except ApiException as e:
                                print("(rotation_secrets)Exception when calling CoreV1Api->patch_namespaced_secret: %s\n" % e)

    def rotation(self):
        #squirrel = sqrl()
        crds = client.CustomObjectsApi()
        nutcrackers = crds.list_cluster_custom_object(self.squirrel.domain_api, self.squirrel.api_version, 'nutcrackers')["items"]
        secrets = self.squirrel.v1.list_secret_for_all_namespaces(watch=False)
        id_rotation = self.randomStringDigits(8)
        if not self.squirrel.debug:
            #self.clean_nuts(id_rotation, "id_clean")
            self.clean_nuts(id_rotation, "old_nutcracker_clean")
        for s in secrets.items:
            if s.metadata.annotations:
                for a in s.metadata.annotations:
                    if a == "squirrel_rotation_app" and s.metadata.annotations[a] == "true":
                        squirrel_user_key = s.metadata.annotations.get("squirrel_username_key", False)
                        squirrel_pass_key = s.metadata.annotations.get("squirrel_password_key", False)
                        squirrel_user = s.data.get(squirrel_user_key, False)
                        squirrel_pass = s.data.get(squirrel_pass_key, False)
                        squirrel_service = s.metadata.annotations.get("squirrel_service", False)
                        squirrel_name = s.metadata.name
                        squirrel_namespace = s.metadata.namespace
                        squirrel_type_frontend = s.metadata.annotations.get("squirrel_type_frontend", False)
                        squirrel_type_backend = s.metadata.annotations.get("squirrel_type_backend", False)
                        squirrel_length_random = s.metadata.annotations.get("squirrel_length_random", self.squirrel_length_random)

                        if squirrel_user_key and squirrel_pass_key and \
                          squirrel_service and squirrel_type_frontend and \
                          squirrel_type_backend and squirrel_user and squirrel_pass:
                            print("(rotation)[INFO] Process %s, namespace %s" % (squirrel_name, squirrel_namespace))
                            random_pass = self.randomStringDigits(squirrel_length_random)

                            # Check app
                            check_app = False
                            if self.check_pods(s.metadata.annotations["squirrel_delete_pods"], s.metadata.namespace):
                                aup = app_update_pass(squirrel_service,
                                                      squirrel_namespace,
                                                      squirrel_user,
                                                      squirrel_pass,
                                                      squirrel_type_frontend,
                                                      squirrel_type_backend,
                                                      s.metadata.annotations,
                                                      "check_app",
                                                      random_pass,
                                                      self.squirrel.squirrel_nuts_manager,
                                                      s,
                                                      self.squirrel.debug)
                                result_aup_conditional = aup.conditional_app()

                                if result_aup_conditional != {}:
                                    if result_aup_conditional.get("%s/%s" % (squirrel_type_frontend, squirrel_type_backend), False):
                                        if result_aup_conditional["%s/%s" % (squirrel_type_frontend, squirrel_type_backend)]["check_app"] == None:
                                            check_app = False
                                        else:
                                            check_app = result_aup_conditional["%s/%s" % (squirrel_type_frontend, squirrel_type_backend)]["check_app"]

                            if check_app:
                                print("(rotation)[INFO] OK Check app: name=%s namespace=%s app_type=%s/%s" % (squirrel_name, 
                                    squirrel_namespace, squirrel_type_frontend, squirrel_type_backend))
                                create_nut = False
                                for nc in nutcrackers:
                                    permissions_fail = True
                                    for p in nc["permissions"]:
                                        permissions = p.split("/")
                                        #print(permissions)
                                        #print("%s %s" % (squirrel_namespace, squirrel_service))
                                        if (permissions[0] == squirrel_namespace and \
                                          permissions[1] == squirrel_service) or \
                                          (permissions[0] == '*' and permissions[1] == '*') or \
                                          (permissions[0] == squirrel_namespace and permissions[1] == '*'):
                                            nut_email = nc["data"]["email"]
                                            nut_nutcracker = nc["metadata"]["name"]
                                            print("(rotation)[INFO] Create nut for %s, nutcracker: %s" % (nut_email, nut_nutcracker))

                                            nut_keypub = nc["data"]["keypub"]
                                            #nc["permissions"]
                                            self.importKey(False, base64.b64decode(nut_keypub))
                                            secret_text = self.encryptText(nut_email, random_pass)

                                            md5_unique_name = hashlib.new('md5')
                                            string_md5 = '%s-%s-%s-%s-%s' % (squirrel_service, squirrel_name, squirrel_namespace, nut_email, nut_nutcracker)
                                            md5_unique_name.update(string_md5.encode())

                                            old_md5_unique_name = hashlib.new('md5')
                                            old_string_md5 = '%s-%s-%s-%s' % (squirrel_service, squirrel_name, squirrel_namespace, nut_email)
                                            old_md5_unique_name.update(old_string_md5.encode())

                                            metadata = {'name': md5_unique_name.hexdigest(), 'namespace': squirrel_namespace}
                                            #metadata = {'name': nut_nutcracker, 'namespace': squirrel_namespace}

                                            new_nut = {}
                                            new_nut = dict(self.squirrel.squirrel_body)
                                            new_nut["metadata"] = metadata
                                            new_nut["kind"] = "Nuts"
                                            new_nut["data"]["nut"] = base64.b64encode(secret_text.encode()).decode()
                                            new_nut["data"]["email"] = nut_email
                                            new_nut["data"]["pcmac"] = nc["data"].get("pcmac", "<none>")
                                            new_nut["data"]["nutcracker"] = nut_nutcracker
                                            new_nut["data"]["squirrel_name"] = squirrel_name
                                            new_nut["data"]["squirrel_service"] = squirrel_service
                                            new_nut["data"]["id_rotation"] = id_rotation

                                            #import pdb; pdb.set_trace()
                                            #print(nut_nutcracker)
                                            if self.check_pods(s.metadata.annotations["squirrel_delete_pods"], s.metadata.namespace):
                                                check_pod_fail = False
                                                if not self.squirrel.debug:

                                                    try:
                                                        # New md5 name
                                                        api_response = crds.delete_namespaced_custom_object(\
                                                            self.squirrel.domain_api, \
                                                            self.squirrel.api_version, \
                                                            squirrel_namespace, \
                                                            'nuts', \
                                                            md5_unique_name.hexdigest(),
                                                            client.V1DeleteOptions())
                                                        #print(api_response)
                                                    except ApiException as e:
                                                        print("(rotation)Exception when calling CustomObjectsApi->delete_namespaced_custom_object: %s\n" % e)
                                                    
                                                    try:
                                                        # Old md5 name
                                                        crds.delete_namespaced_custom_object(\
                                                            self.squirrel.domain_api, \
                                                            self.squirrel.api_version, \
                                                            squirrel_namespace, \
                                                            'nuts', \
                                                            old_md5_unique_name.hexdigest(),
                                                            client.V1DeleteOptions())
                                                    except ApiException as e:
                                                        print("(rotation) Try delete old nuts: %s\n" % e)

                                                    try:
                                                        api_response = crds.create_namespaced_custom_object(\
                                                            self.squirrel.domain_api, \
                                                            self.squirrel.api_version, \
                                                            squirrel_namespace, \
                                                            'nuts', \
                                                            new_nut)
                                                        print("(rotation) Nut %s: %s for %s" % (new_nut["metadata"]["name"], secret_text, nut_email))
                                                    except ApiException as e:
                                                        print("Exception when calling CustomObjectsApi->create_namespaced_custom_object: %s\n" % e)
                                                    permissions_fail = False

                                                else:
                                                   permissions_fail = False 
                                            else:
                                                check_pod_fail = True 
                                    if check_pod_fail:
                                        print("(rotation)[INFO] No rotate %s, are the pods standing? namespace %s" % (squirrel_service, squirrel_namespace)) 
                                    else:
                                        if permissions_fail:
                                            print("(rotation)[INFO] No have permissions in %s, namespace %s" % (squirrel_service, squirrel_namespace))
                                        else:
                                            print("(rotation)[INFO] Permissions in %s, namespace %s" % (squirrel_service, squirrel_namespace))
                                            create_nut = True
                                if not check_pod_fail:
                                    if create_nut:
                                        aup = app_update_pass(squirrel_service,
                                                              squirrel_namespace,
                                                              squirrel_user,
                                                              squirrel_pass,
                                                              squirrel_type_frontend,
                                                              squirrel_type_backend,
                                                              s.metadata.annotations,
                                                              "update_app_password",
                                                              random_pass,
                                                              self.squirrel.squirrel_nuts_manager,
                                                              s,
                                                              self.squirrel.debug)
                                        aup.conditional_app()
                                    else:
                                        if not self.squirrel.debug:
                                            print("(rotation)[INFO] Not found nutcrackers for secret %s" % (s.metadata.name,
                                                                                                  s.metadata.namespace))
                            else:
                                print("(rotation)[ERROR] Check app: name=%s namespace=%s app_type=%s/%s" % (squirrel_name, 
                                    squirrel_namespace, squirrel_type_frontend, squirrel_type_backend))
                        else:
                            print("(rotation)[ERROR] in %s, namespace %s" % (squirrel_name, squirrel_namespace))
