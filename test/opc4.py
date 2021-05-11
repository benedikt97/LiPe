#!/usr/bin/python3
print("opc.py being executed")

import sys
import json
import mariadb
import time
import LiPe as lp
import LiPeDB as lpd
from opcua import Client

sys.path.insert(0, "..")

def connectopc():
    try:
        global client
        client = Client(configjs["IP"])
        client.connect()
        
        print("OPC Server connected at: " + configjs["IP"])
    except Exception as e:
        dbconn.writecom("opc", "Error", "No Connection to OPC Server possible", str(e))


      
         

def readdata():
    dbconn.writecom("opc", "Running", "Collecting Data", "")
    actValues = {}
    while True:
        comma = False
        try:
            for id in nodesjs:          
                node = client.get_node(nodesjs[id])
                value = node.get_value()     
                actValues[id] = value                
            dbconn.WriteActValues(actValues)
            print("collected")
        except Exception as e:
            dbconn.writecom("opc", "Error", "No Connection to OPC Server/Database possible", str(e))
            return()
        
        #time.sleep(configjs["Zyklus"])


    


def cycle():
    global dbconn
    dbconn = lpd.dbcon("LiPe", "127.0.0.1", "opc", "LiPePWD320"))
    dbconn.prepareAndSelectLoggingTable("Cola")
    print("DB Prepared")
    global configjs
    configjs = lp.loadconfig()
    global nodesjs
    nodesjs = lp.loadnodes()
    print("Config Loaded)")
    connectopc()
    print("Opc Connected")
    readdata()
    


    


if __name__ == "__main__":
    cycle()

    
    
   
    
   



