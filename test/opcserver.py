import sys
sys.path.insert(0, "../app")
import time
import LiPe


from opcua import ua, Server


if __name__ == "__main__":

    # setup our server
    server = Server()
    server.set_endpoint("opc.tcp://127.0.0.1:4840/freeopcua/server/")

    # setup our own namespace, not really necessary but should as spec
    uri = "http://examples.freeopcua.github.io"
    idx = server.register_namespace(uri)

    # get Objects node, this is where we should put our nodes
    objects = server.get_objects_node()

    # populating our address space
    myobj = objects.add_object(idx, "WS_TestNodes")
    totBottles = myobj.add_variable(idx, "Total_Bottles", 0)
    curMachSpeed = myobj.add_variable(idx, "Cur_MachSpeed", 120000)
    setMachSpeed = myobj.add_variable(idx, "Set_MachSpeed", 120000)
    curMode = myobj.add_variable(idx, "Cur_Mode", 32)
    curProgramm = myobj.add_variable(idx, "Cur_Programm", 8)
    curState = myobj.add_variable(idx, "Cur_State", 2)
    levelBowl = myobj.add_variable(idx, "Level_Bowl", 70)
    pressBowl = myobj.add_variable(idx, "Press_Bowl", 4.5)
    pressProduct = myobj.add_variable(idx, "Press_Product", 5.2)
    pressReturnGas = myobj.add_variable(idx, "Press_ReturnGas", 2.3)
    pressWater = myobj.add_variable(idx, "Press_Water", 8.2)
    designSpeed = myobj.add_variable(idx, "Design_Speed", 120000)
    
    
    
    
    
    
    # myvar.set_writable()    # Set MyVariable to be writable by clients

    # starting!
    server.start()
    
    try:
        count = 0
        while True:
            time.sleep(1)
            count += 1
            totBottles.set_value(count)
    finally:
        #close connection, remove subcsriptions, etc
        server.stop()