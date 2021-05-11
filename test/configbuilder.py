#!/usr/bin/python
print("configbuilder being executed")

import sys
sys.path.insert(0, "..")
import json




if __name__ == "__main__":

    settings = {'IP':'opc.tcp://192.168.132.51:4840', 'Zyklus': 1, 'Command': "wait", 'DBName' : 'lipo', 'DBUser' : 'lipo', 'DBPassword' : 'lipo',}
    with open('..//config/config.json', 'w+') as fp:
        json.dump(settings, fp)

    with open('../config/config.json', 'r') as fp:
        data = json.load(fp)
    print(data)
    print(type(data)) 



