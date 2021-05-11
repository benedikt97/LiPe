import LiPeOPC as lpo
import LiPe as lp
import time

configjs = lp.loadopcconfig()
nodesjs = lp.loadnodes()


opc = lpo.opccon(configjs, nodesjs)
opc.collect(False)
print("Still executing...")
time.sleep(4)
print(opc.getActValues())
time.sleep(4)
print(opc.getActValues())
time.sleep(4)
print(opc.getActValues())
time.sleep(4)
print(opc.getActValues())
time.sleep(4)
opc.collect(False)
print(opc.getActValues())
time.sleep(4)
print(opc.getActValues())
time.sleep(4)
opc.stopcollect()
print("Collecting Stopped")