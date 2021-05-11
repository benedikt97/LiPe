#!/usr/bin/python3
import json
import mariadb


def loadopcconfig():
    f = open("./config/opcconfig.json")
    configjs = json.load(f)
    f.close()
    return (configjs)

def loadnodes():
    f = open("./config/nodes.json")
    nodesjs = json.load(f)
    f.close()
    return nodesjs

def loadserverconfig():
    f = open("./config/serverconfig.json")
    configjs = json.load(f)
    f.close()
    return (configjs)




            




