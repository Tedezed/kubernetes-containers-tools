#!/usr/bin/python3
# -*- coding: utf-8 -*-

# By: Juan Manuel Torres (Tedezed)
# Source: https://github.com/Tedezed
# Mail: juanmanuel.torres@aventurabinaria.es

from sys import argv
from copy import deepcopy

from chronos import *
from module_control import *

debug = True

def argument_to_dic(list):
    dic = {}
    for z in list:
        dic[z[0]] = z[1]
    return dic

def main():
    list_argv = []
    argv_ext = deepcopy(argv)

    argv_ext.remove(argv_ext[0])
    for elements in argv_ext:
        var_input = elements.split("=")
        if len(var_input) == 1 or var_input[1] == '':
            raise NameError('[ERROR] (main) Invalid Arguments [python example.py var="text"]')
        list_argv.append(var_input)
    dic_argv = argument_to_dic(list_argv)

    chronos_backup = chronos(debug)
    chronos_backup.check_disk("/backup-db-cron/backups")

    if dic_argv.get("mode", False) == "databases":
        try:
            chronos_backup.start_chronos()
        except Exception as error:
            print("[ERROR] (main) backup databases %s" % str(error))
            logging.error(error)
            send_mail("[ERROR DATABASES] Mode %s" \
              % ("databases backup"), str(error).replace("<","").replace(">",""), debug)
        
    elif dic_argv.get("mode", False) == "disks":
        try:
            #chronos_backup.snapshot()
            chronos_backup.start_chronos()
        except Exception as error:
            print("[ERROR] (main) disks snapshot %s" % str(error))
            logging.error(error)
            send_mail("[ERROR DISKS] Mode %s" \
              % ("disks snapshot"), str(error).replace("<","").replace(">",""), debug)
    else:
        print("[ERROR] (main) Mode not found")

if __name__ == '__main__':
    # Start
    main()
