# -*- coding: UTF-8 -*-

import sys
import os
import random

import logging.config
import logging.handlers
import logging
from pkgs.atp_main import AtpControl
from log import log_config
'''
lsc main process 
'''
def LscProcess(inputdata, outputdata, standard):
    inputdataa = inputdata.copy()
    outputdataa = outputdata.copy()
    standarda = standard
    CheckType = LscCheckType(inputdataa, standarda)    #check  issue type
    #print("inputdata:", inputdataa, "\noutputdata:", outputdata, "\nCheckType_fail", CheckType)

    if CheckType == "Y_Shading":
        OutputParam = YShadingProcess(inputdataa, outputdataa, standarda)   #Y Shading  process
    elif CheckType == "Color_Shading":
        OutputParam = ColorShadingProcess(inputdataa, outputdataa, standarda)  #Color Shading  process
    elif CheckType == "AWB":
        return "AWB_issue"
    else:
        print("don't check issue type !!!")
        return "ERROR"

    return OutputParam

def YShadingProcess(YSinputdata, param, standard):
   if YSinputdata[1] <= standard:
       param[0] = 100
       param[1] = 100
       param[2] = 100
   elif YSinputdata[1] >= (standard + 15):
       param[0] = -100
       param[1] = -100
       param[2] = -100
   else:
       param[0] = 0
       param[1] = 0
       param[2] = 0

   return param

def ColorShadingProcess(CSinputdata, param, standard):
    # check Y Shading  pass?
    for i in range(1, len(CSinputdata)):
        for j in range(len(param)):
            #print("dddd", CSinputdata, i, CSinputdata[i])
            if float(CSinputdata[i]) < standard[0]:
                param[i-1] = 100
            elif float(CSinputdata[i]) > standard[1]:
                param[i-1] = -100
            else:
                param[i-1] = 0

    return param

def LscCheckType(lscinput,standard):
    inputdata = lscinput

    if inputdata[0] == "Y-Shading":
        Check_Type = "Y_Shading"
        return Check_Type
    elif inputdata[0] == "Color-Shading":
        r_g_avg = (inputdata[1] + inputdata[2]) / 2
        b_g_avg = (inputdata[3] + inputdata[4]) / 2
        r_g_sub = (abs(inputdata[1] - inputdata[2])) / 2
        b_g_sub = (abs(inputdata[3] - inputdata[4])) / 2
        c_v = (standard[0] - standard[1]) / 2  # 0.10000000000000003
        print("r-b value:", r_g_avg, b_g_avg, r_g_sub, b_g_sub, "c_v", c_v)
        if r_g_avg < standard[0] or r_g_avg > standard[1] or b_g_avg < standard[0] or b_g_avg > standard[1]:
            Check_Type = "AWB"
            return Check_Type
        elif r_g_sub > c_v or b_g_sub > c_v:
            Check_Type = "Color_Shading"
            return Check_Type
        else:
            Check_Type = None
            return Check_Type

    else:
        return "ERROR"

def GetLscData():
    max_standard = 1.1
    min_satndard = 0.9
    Y_standard = 75

    inputdatatype = random.choice(["Y-Shading", "Color-Shading"])

    if inputdatatype == "Y-Shading":
        inputdata = ["Y-Shading", random.randrange(30, 110, 5)]
        outputdata = ["light_D", "light_C", "light_A"]
        standard = Y_standard
    else:
        inputdata = ["Color-Shading", random.randrange(7, 15, 1) / 10, random.randrange(7, 15, 1) / 10,
                     random.randrange(7, 15, 1) / 10, random.randrange(7, 15, 1) / 10]
        outputdata = ["level_r", "level_b", "weight_r", "weight_b"]
        standard = [min_satndard, max_standard]

    return inputdata, outputdata, standard


def adapt_lsc():
    log_config()
    logger = logging.getLogger("lsc_main")
    lsc = AtpControl()
    lsc.setFlag(1)

    logger.info("start lsc !!! \n")
    for k in range(10):
        inputdata, outputdata, standard = GetLscData()
        outputparamweight = LscProcess(inputdata, outputdata, standard)
        #SetOutputParam(outputparamweight)
        f = open("./logs/atp_all.log", 'w+')
        print("-----------\nnum:", k, "\ninputdata:", inputdata, "\noutputdata:", outputdata, "\nstandard:", standard, "\noutputparamweight:", outputparamweight, "\n")
    logger.info("end  lsc !!!")

def main():
    atp = AtpControl()
    while atp.getFlag() == 0:
        break
    atp.setFlag(1)

    while atp.getFlag() == 0:
        break
    atp.setFlag(1)
    adapt_lsc()
    return

if __name__ == "__main__":
    main()

