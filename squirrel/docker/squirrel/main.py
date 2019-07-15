#!/usr/bin/python3

# password rotation (Squirrel, Nuts Warehouse)
# By Tedezed

import gnupg, random, string, re, json
from kubernetes import client, config
from os import path, getlogin, system, getuid, environ
from sys import argv
from getpass import getpass
import base64

from controller.controller import *
from nuts_manager.nuts_manager import *

gnupg._parsers.Verify.TRUST_LEVELS["ENCRYPTION_COMPLIANCE_MODE"] = 23

class sqrl():

    # Basic
    ruta_exec = path.dirname(path.realpath(__file__))
    squirrel_away = "%s/away" % ruta_exec
    squirrel_controller = "%s/controller" % ruta_exec
    len_password = 22
    nut_list = []
    nuts = {}
    try:
        if environ["DEBUG"] == "True":
            debug = True
        else:
            debug = False
    except:
        debug = False

    # Controller
    domain_api = "tree.squirrel.local"
    api_version = "v1"
    squirrel_body = {'metadata': {}, 'apiVersion': 'tree.squirrel.local/v1', \
        'type': 'Opaque', 'data': {}}

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
            # try:
            #     config.load_kube_config()
            # except OSError:
            #     config.load_kube_config(config_file='/home/%s/.kube/config-slug' % (pwd.getpwuid(getuid()).pw_name))
            pass
        else:
            config.load_incluster_config()

        # Define Kubernetes API
        self.v1 = client.CoreV1Api()
        self.extv1beta1 = client.ExtensionsV1beta1Api()

def main():
    squirrel = sqrl()
    nm = nuts_manager(squirrel)
    if squirrel.dic_argv.get("mode", False) == "controller":
        ct = controller(squirrel)
        ct.daemon_controller()
    elif squirrel.dic_argv.get("mode", False) == "cronjob":
        print("[INFO] Exec rotation credentils for apps")
        nm.rotation()
        print("[INFO] Exec rotation secrets")
        nm.rotation_secrets()
    elif squirrel.dic_argv.get("mode", False) == "client-create-key":
        pass_not_ok = True
        while pass_not_ok:
            key_pass = getpass("Password: ")
            key_pass_copy = getpass("Enter the password again: ")
            if key_pass == key_pass_copy:
                pass_not_ok = False
                key_file = squirrel.dic_argv.get("key-file", False)
                email = squirrel.dic_argv.get("email", False)
                bits = squirrel.dic_argv.get("bits", 4096)
                if email and key_file:
                    nm.createKey(
                        key_file,
                        email,
                        key_pass,
                        bits,
                        "RSA"
                    )
                else:
                    print("Use: mode='client-create-key' key-file='local.pub' email='admin@example.com'")
            else:
                print("Passwords do not match...")
    elif squirrel.dic_argv.get("mode", False) == "import-key":
        key_file = squirrel.dic_argv.get("key-file", False)
        if key_file:
            nm.importKey(key_file)
        else:
            print("Use: mode='import-key' key-file='local.pub'")
    elif squirrel.dic_argv.get("mode", False) == "decrypt-text":
        # Decrypt for client
        encrypted_string = squirrel.dic_argv.get("encrypted-string", False)
        if encrypted_string:
            key_pass = getpass()
            print(nm.dencryptText(key_pass, encrypted_string, "base64"))
        else:
            print("Use: mode='decrypt-text' encrypted-string='XXXXXXXXX'")
    elif squirrel.dic_argv.get("mode", False) == "encrypt-text":
        email = squirrel.dic_argv.get("email", False)
        text = squirrel.dic_argv.get("text", False)
        if email:
            print(nm.encryptText(email, text))
        else:
            print("Use: mode='encrypt-text' email='admin@example.com' text='hello!'")
    elif squirrel.dic_argv.get("mode", False) == "list-keys":
        print(squirrel.gpg.list_keys())
    else:
        print("Use: mode=(controller or cronjob)")

if __name__ == '__main__':
    # Start
    main()