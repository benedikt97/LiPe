#!/usr/bin/python
print("configbuilder being executed")

import sys
sys.path.insert(0, "..")
import json




if __name__ == "__main__":

    settings = {
    'WS_Tot_Bottles':'ns=3;s="WS_Data_DB"."WS_Tot_Bottles"',
    'WS_Cur_Mach_Spd': 'ns=3;s="WS_Data_DB"."WS_Cur_Mach_Spd"',
    'WS_Set_Mach_Spd': 'ns=3;s="WS_Data_DB"."WS_Set_Mach_Spd"',
    'WS_Cur_Mode' : 'ns=3;s="WS_Data_DB"."WS_Cur_Mode"',
    'WS_Cur_Program' : 'ns=3;s="WS_Data_DB"."WS_Cur_Prog"',
    'WS_Cur_State' : 'ns=3;s="WS_Data_DB"."WS_Cur_State"',
    'WS_Press_Bottling' : 'ns=3;s="WS_Data_DB"."WS_Press_Bottling"',
    'WS_Temp_Bottling' : 'ns=3;s="WS_Data_DB"."WS_Temp_Bottling"',
    'KHS_Level_Bowl' : 'ns=3;s="WS_Data_DB"."KHS_Level_Bowl"',
    'ActiveEnergyRate1' : 'ns=3;s="LibKHS_EnergyToHMI_DB"."MeasuringValues"."ActiveEnergyRate1"'}
        
    with open('../config/nodes.json', 'w+') as fp:
        json.dump(settings, fp)

    with open('../config/nodes.json', 'r') as fp:
        data = json.load(fp)
    print(data)
    print(type(data)) 



