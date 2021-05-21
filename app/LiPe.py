#!/usr/bin/python3
import json



def loadopcconfig():
    f = open("./app/config/opcconfig.json")
    configjs = json.load(f)
    f.close()
    return (configjs)

def loadnodes():
    f = open("./app/config/nodes.json")
    nodesjs = json.load(f)
    f.close()
    return nodesjs

def loadserverconfig():
    f = open("./app/config/serverconfig.json")
    configjs = json.load(f)
    f.close()
    return (configjs)




            




