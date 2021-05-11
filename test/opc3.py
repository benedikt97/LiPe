#!/usr/bin/python3
print("opc.py being executed")

import sys
import json
import mariadb
import time
import threading
from opcua import Client
from pystalk import BeanstalkClient
sys.path.insert(0, "..")




def loadconfig():
    f = open("./config/config.json")
    global configjs
    configjs = json.load(f)
    f.close()

def loadnodes():
    f = open("./config/nodes.json")
    global nodesjs
    nodesjs = json.load(f)
    f.close()

def loadcom():
    f = open("/var/www/html/LinePerformance/com.json")
    global comjs
    comjs = json.load(f)
    f.close()

def writecom(state, message, exception):
    comjs = {}
    comjs['State'] = state
    comjs['Message'] = message
    comjs['Exception'] = exception
    with open('/var/www/html/LinePerformance/com.json', 'w+') as fp:
    #with open('./com.json', 'w+') as fp:
        json.dump(comjs, fp)
    return;

def connectopc():
    try:
        global client
        client = Client(configjs["IP"])
        client.connect()
        
        print("OPC Server connected at: " + configjs["IP"])
    except Exception as e:
        writecom("Error", "No Connection to OPC Server possible", str(e))

def connectdb():
    try:
        global conn
        conn = mariadb.connect(
            user = configjs["DBUser"],
            password = configjs["DBPassword"],
            host = configjs["DBAdress"],
            port = 3306,
            database = configjs["DBName"]
        )
        global cur
        cur = conn.cursor()
        # Prepare database
        sql = "DROP TABLE IF EXISTS " + configjs["DBTablename"]
        cur.execute(sql)
        sql = "CREATE TABLE " + configjs["DBTablename"] + " (id INT AUTO_INCREMENT PRIMARY KEY)"   
        cur.execute(sql)
        sql = "ALTER TABLE " + configjs["DBTablename"] + " ADD COLUMN " + "Time" + " TIMESTAMP"
        cur.execute(sql)
        for id in nodesjs:
            sql = "ALTER TABLE " + configjs["DBTablename"] + " ADD COLUMN " + id + " FLOAT NOT NULL DEFAULT 0"
            cur.execute(sql)
        cur.execute("SHOW TABLES")
        sql = "INSERT INTO " + configjs["DBTablename"] + " ("
        comma = False
        for id in nodesjs:
            if comma:
                sql = sql + ", "
            sql = sql + id
            comma = True
        comma = False 
        global sqlpre
        sqlpre = sql + ") VALUES ("  
    except mariadb.Error as e:
        writecom("Error", "Connection to Database not possible", str(e))
      
         

def readdata(stop):
    writecom("Logging", "Nodes getting collected to Database", "")
    actValues = {}
    while True:
        comma = False
        try:
            for id in nodesjs:          
                node = client.get_node(nodesjs[id])
                value = node.get_value()  
                if comma:
                    sql = sql + ", "
                else:
                    sql = sqlpre
                    comma = True 
                sql = sql + str(value)    
                actValues[id] = value                
            comma = False
            sql = sql + ")"
            print(sql)
            cur.execute(sql)
            conn.commit()
            if stop():
                break
        except Exception as e:
            writecom("Error", "OPC/Database Connection Failed", str(e))
            return()
        
        time.sleep(configjs["Zyklus"])

        


def executejob(job):
    command = str(job.job_data)
    print("Executing Command")
    if "init" in command:
        loadconfig()
        loadnodes()
        connectopc()
        connectdb()
    elif "run" in command:      
        x = threading.Thread(target=readdata)
        x.start()
    #elif "stop" in command:
        
    else:
        print("Command not Found")
        return
    return
    
    


def cycle():
    try:
        job = btclient.reserve_job(1)        
    except:
        print("No jobs Available")
        job=""
    
    if (job!=""):
        print(job.job_data)
        executejob(job)    
        btclient.delete_job(job.job_id)
        print("Deleting Command")
    


    


if __name__ == "__main__":
    global btclient 
    btclient = BeanstalkClient('127.0.0.1', 11300)
    
    
    while(True):
        cycle()

    
    
   
    
   



