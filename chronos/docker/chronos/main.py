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

    chronos_backup = chronos(dic_argv, debug)
    chronos_backup.check_disk("/chronos/backups")

    try:
        chronos_backup.start_chronos()
    except Exception as error:
        print("[ERROR] (main) %s" % str(error))
        logging.error(error)
        send_mail("[ERROR] Mode %s" \
            % ("(main)"), str(error).replace("<","").replace(">",""), debug)

    else:
        print("[ERROR] (main) Mode not found")

if __name__ == '__main__':
    # Start
    main()
