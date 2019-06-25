#!/usr/bin/python3

# By Tedezed
# https://www.saltycrane.com/blog/2011/10/python-gnupg-gpg-example/
# https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/ApiextensionsV1beta1Api.md

import gnupg, random, string, re, json
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from os import path, getlogin, system, getuid, environ
from sys import argv
import base64, hashlib

from .app_update_pass import *

class nuts_manager():

    def __init__(self, squirrel):
        self.squirrel = squirrel
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
        input_data = self.squirrel.gpg.gen_key_input(
            key_type=keytype,
            key_length=keylen,
            name_email=email,
            passphrase=password)
        key = self.squirrel.gpg.gen_key(input_data)
        print("Key: ", key)
        self.exportKey(keyfile, str(key.fingerprint))

    def exportKey(self, keyfile, key):
        ascii_armored_public_keys = self.squirrel.gpg.export_keys(key)
        ascii_armored_private_keys = self.squirrel.gpg.export_keys(key, secret=True)
        with open("%s.pub" % keyfile, 'w') as f:
            f.write(ascii_armored_public_keys)
        with open("%s.key" % keyfile, 'w') as f:
            f.write(ascii_armored_private_keys)

    def importKey(self, keyfile, key_data=False):
        if keyfile:
            key_data = open(keyfile).read()
        print(key_data)
        import_result = self.squirrel.gpg.import_keys(key_data)
        print(import_result.results)

    def encryptText(self, email, text_to_encrypt):
        encrypted_data = self.squirrel.gpg.encrypt(text_to_encrypt, email, always_trust=True)
        encrypted_string = str(encrypted_data)
        #print(encrypted_data)
        print('ok: ', encrypted_data.ok)
        print('status: ', encrypted_data.status)
        #print('stderr: ', encrypted_data.stderr)
        #print('unencrypted_string: ', text_to_encrypt)
        #print('encrypted_string: ', encrypted_string)
        return encrypted_string

    def dencryptText(self, password, encrypted_string, mode=False):
        if mode == "base64":
            print("Mode input base64")
            print(encrypted_string)
            print(base64.b64decode(encrypted_string + '=' * (-len(encrypted_string) % 4)).decode())
            decrypted_data = self.squirrel.gpg.decrypt(\
                str(base64.b64decode(encrypted_string + '=' * (-len(encrypted_string) % 4)).decode()),\
                passphrase=password)
        else:
            decrypted_data = self.squirrel.gpg.decrypt(encrypted_string, passphrase=password)
        print('ok: ', decrypted_data.ok)
        print('status: ', decrypted_data.status)
        #print('stderr: ', decrypted_data.stderr)
        #print('decrypted string: ', decrypted_data.data)
        return str(decrypted_data.data)

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

    def rotation(self):
        #squirrel = sqrl()
        crds = client.CustomObjectsApi()
        nutcrackers = crds.list_cluster_custom_object(self.squirrel.domain_api, self.squirrel.api_version, 'nutcrackers')["items"]
        secrets = self.squirrel.v1.list_secret_for_all_namespaces(watch=False)
        for s in secrets.items:
            if s.metadata.annotations:
                for a in s.metadata.annotations:
                    if a == "squirrel" and s.metadata.annotations[a] == "true":
                        squirrel_user_key = s.metadata.annotations.get("squirrel_username_key", False)
                        squirrel_pass_key = s.metadata.annotations.get("squirrel_password_key", False)
                        squirrel_user = s.data.get(squirrel_user_key, False)
                        squirrel_pass = s.data.get(squirrel_user_key, False)
                        squirrel_service = s.metadata.annotations.get("squirrel_service", False)
                        squirrel_name = s.metadata.name
                        squirrel_namespace = s.metadata.namespace
                        squirrel_type_frontend = s.metadata.annotations.get("squirrel_type_frontend", False)
                        squirrel_type_backend = s.metadata.annotations.get("squirrel_type_backend", False)

                        if squirrel_user_key and squirrel_pass_key and \
                          squirrel_service and squirrel_type_frontend and \
                          squirrel_type_backend and squirrel_user and squirrel_pass:
                            print("[INFO] Process %s, namespace %s" % (squirrel_name, squirrel_namespace))
                            random_pass = self.randomStringDigits(26)
                            for nc in nutcrackers:
                                permissions_fail = True
                                for p in nc["permissions"]:
                                    permissions = p.split("/")
                                    #print(permissions)
                                    #print("%s %s" % (squirrel_namespace, squirrel_service))
                                    if permissions[0] == squirrel_namespace and \
                                      permissions[1] == squirrel_service:
                                        permissions_fail = False
                                        nut_email = nc["data"]["email"]
                                        print("[INFO] Create nut for %s" % nut_email)

                                        nut_keypub = nc["data"]["keypub"]
                                        #nc["permissions"]
                                        self.importKey(False, base64.b64decode(nut_keypub))
                                        secret_text = self.encryptText(nut_email, random_pass)

                                        md5_unique_name = hashlib.new('md5')
                                        string_md5 = '%s-%s-%s-%s' % (squirrel_service, squirrel_name, squirrel_namespace, nut_email)
                                        md5_unique_name.update(string_md5.encode())
                                        metadata = {'name': md5_unique_name.hexdigest(), 'namespace': squirrel_namespace}
                                        #metadata = {'name': nc["metadata"]["name"], 'namespace': squirrel_namespace}

                                        new_nut = dict(self.squirrel.squirrel_body)
                                        new_nut["metadata"] = metadata
                                        new_nut["kind"] = "Nuts"
                                        new_nut["data"]["nut"] = base64.b64encode(secret_text.encode()).decode()
                                        new_nut["data"]["email"] = nut_email
                                        new_nut["data"]["squirrel_name"] = squirrel_name
                                        new_nut["data"]["squirrel_service"] = squirrel_service

                                        #import pdb; pdb.set_trace()
                                        print(nc["metadata"]["name"])
                                        try:
                                            api_response = crds.delete_namespaced_custom_object(\
                                                self.squirrel.domain_api, \
                                                self.squirrel.api_version, \
                                                squirrel_namespace, \
                                                'nuts', \
                                                md5_unique_name.hexdigest(),
                                                client.V1DeleteOptions())
                                            print(api_response)
                                        except ApiException as e:
                                            print("Exception when calling CustomObjectsApi->delete_namespaced_custom_object: %s\n" % e)

                                        try:
                                            api_response = crds.create_namespaced_custom_object(\
                                                self.squirrel.domain_api, \
                                                self.squirrel.api_version, \
                                                squirrel_namespace, \
                                                'nuts', \
                                                new_nut)
                                            print("Nut %s for %s" % (secret_text, nut_email))
                                        except ApiException as e:
                                            print("Exception when calling CustomObjectsApi->create_namespaced_custom_object: %s\n" % e)

                                        # End
                                        aup = app_update_pass(squirrel_service, \
                                                            squirrel_namespace, \
                                                            squirrel_user, \
                                                            squirrel_pass, \
                                                            squirrel_type_frontend, \
                                                            squirrel_type_backend,
                                                            s.metadata.annotations,
                                                            random_pass)
                                        aup.conditional_app()
                                if permissions_fail:
                                    print("[INFO] No have permissions in %s, namespace %s" % (squirrel_service, squirrel_namespace))
                                else:
                                    print("[INFO] Permissions in %s, namespace %s" % (squirrel_service, squirrel_namespace))
                        else:
                            print("[ERROR] in %s, namespace %s" % (squirrel_name, squirrel_namespace))
        exit()
        #squirrel.createKey('mykeyfile', 'juanmanuel.torres@aventurabinaria.es', '1234567890')
        squirrel.importKey('mykeyfile.pub')
        print(squirrel.listKey)
        secret_text = squirrel.encryptText('juanmanuel.torres@aventurabinaria.es', squirrel.randomStringDigits(22))
        print(secret_text)
        print(squirrel.dencryptText('1234567890', secret_text))

    # def rotation(self):
    #     squirrel = sqrl()
    #     #squirrel.createKey('mykeyfile', 'juanmanuel.torres@aventurabinaria.es', '1234567890')
    #     squirrel.importKey('mykeyfile.pub')
    #     print(squirrel.listKey)
    #     secret_text = squirrel.encryptText('juanmanuel.torres@aventurabinaria.es', squirrel.randomStringDigits(22))
    #     print(secret_text)
    #     print(squirrel.dencryptText('1234567890', secret_text))

# def old():
#     squirrel = sqrl()
#     #squirrel.createNut('mykeyfile', 'juanmanuel.torres@aventurabinaria.es', '1234567890')
#     squirrel.importNut('mykeyfile.pub')
#     print(squirrel.listNuts)
#     secret_text = squirrel.encryptText('juanmanuel.torres@aventurabinaria.es', squirrel.randomStringDigits(22))
#     print(secret_text)
#     print(squirrel.dencryptText('1234567890', secret_text))


# def main():
#     squirrel = sqrl()
#     squirrel.away()

# if __name__ == '__main__':
#     # Start
#     main()