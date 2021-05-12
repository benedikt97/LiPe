#!/usr/bin/python3
import subprocess
import time

print("opc.py being executed")


appsub = subprocess.Popen(['python3', 'app/AppServer.py'])

time.sleep(600)

#print("Killing Server")
#appsub.kill()
#print("Server Killed")




