#!/usr/bin/python3
print("opc.py being executed")

import sys
import json
import time
import LiPeDB as lpd
from opcua import Client
from threading import Thread

sys.path.insert(0, "..")

class opccoll(Thread):
    def __init__(self, opcconfigjs, nodesjs, opcclient, dbconn, isLogging):
        Thread.__init__(self)
        self.isLogging = isLogging
        self.configjs = opcconfigjs
        self.nodesjs = nodesjs
        self.client = opcclient
        self.dbconn = dbconn      
        try:
            if isLogging:
                self. sqlpre = self.dbconn.prepareAndSelectLoggingTable(self.configjs["DBTablename"], self.nodesjs)        
            self.dbconn.writecom("opc", "Connected", "Connectected succesfully to Database", "")
        except Exception as e:
            self.dbconn.writecom("opc", "Error", "No Connection to Database possible", str(e))
        return   

    def run(self):
        self.isRunning = True
        while self.isRunning:
            self.internActValues = {}       
            try:
                for id in self.nodesjs:          
                    node = self.client.get_node(self.nodesjs[id])
                    value = node.get_value()     
                    self.internActValues[id] = value   
                self.actValues = self.internActValues    
                if self.isLogging:
                    self.dbconn.WriteActValues(self.sqlpre, self.actValues)      
                time.sleep(self.configjs["Zyklus"])  
            except Exception as e:
                self.dbconn.writecom("opc", "Error", "No Connection to OPC Server/Database possible", str(e))
                return
        return

class opccon:
    
    def __init__(self, opcconfigjs, nodesjs):
        self.actValues = {}
        self.dbconn = lpd.dbcon("LiPe", "127.0.0.1", "opc", "LiPePWD320")
        return         

    def initopc(self, opcconfigjs, nodesjs):
        try:
            if self.opcthread.isAlive():
                self.dbconn.writecom("opc", "Error", "Thread is running, please stop Thread for new Configuration", "")
                return
        except:
            dummy = False
        try:
            self.configjs = opcconfigjs
            self.nodesjs = nodesjs
            self.client = Client(self.configjs["IP"])
            self.client.connect()   
            self.dbconn.writecom("opc", "Connected", "Connectected succesfully to " + self.configjs["IP"], "")
        except Exception as e:
            self.dbconn.writecom("opc", "Error", "No Connection to OPC Server", str(e))

    def collect(self, isLogging): 
        try:
            if self.opcthread.isAlive():
                self.dbconn.writecom("opc", "Error", "Thread already running", "")
                return
        except Exception as e:
            self.isLogging = isLogging
            self.opcthread = opccoll(self.configjs, self.nodesjs, self.client, self.dbconn, self.isLogging)
            self.opcthread.start()
            self.dbconn.writecom("opc", "Starting", "Thread Started", str(e))
            return
        
    def stopcollect(self):
        try:
            self.opcthread.isRunning = False
            self.dbconn.writecom("opc", "Starting", "Thread Stopped", "")
        except:
            self.dbconn.writecom("opc", "Error", "Thread not Stopped, no Thread Running", "")

    def getActValues(self):
        try:
            return self.opcthread.actValues
        except Exception as e:
            return str(e)



       


        



    
    



    
    
   
    
   


