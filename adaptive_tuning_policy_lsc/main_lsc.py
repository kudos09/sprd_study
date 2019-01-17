#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
import os
import random
import json, xlwt

import logging.config
import logging.handlers
import logging
from pkgs.atp_main import AtpControl
from log import log_config

'''
lsc main process 
'''


def GetJsonFile(jsfile):
    f = open(jsfile, encoding='utf-8')
    jsonData = json.load(f)
    #Finputdata = json.dumps(jsonData, indent=4, ensure_ascii=False)
    return jsonData


def LscProcess(inputdata, outputdata):
    inputdataa = inputdata
    outputdataa = outputdata

    CheckType = LscCheckType(inputdataa)  # check  issue type
    #print("inputdata:", inputdataa, "\noutputdata:", outputdata, "\nCheckType_fail", CheckType)
    for k in range(len(CheckType)):
        if CheckType[k] == "Y_Shading":
            OutputParam = YShadingProcess(inputdataa, outputdataa)  # Y Shading  process
            print("\nk:", k, OutputParam, CheckType[k])
            output = dict(OutputParam)
        elif CheckType[k] == "Color_Shading":
            OutputParam1 = ColorShadingProcess(inputdataa, outputdataa)  # Color Shading  process
            print("\nk:", k, OutputParam1, CheckType[k])
            #output = output.update(OutputParam1)
        elif CheckType[k] == "AWB":
            OutputParam2 = "AWB_issue"
        else:
            print("don't check issue type !!!")
            OutputParam3 = "ERROR"
    print("output:222", output)
    return output
def YShadingout(outputdata):
    for i in range(len(outputdata['LNC'])):
        param = outputdata['LNC'][i]
    for k in param:
        param[k] = 0
    print("lllll", param)

def YShadingProcess(inputdata, outputdata):
    standard = inputdata['Y-Shading']['D65_700lux']['0.9F']['range_min']
    for i in range(len(outputdata['LNC'])):
        param = outputdata['LNC'][i]
        for k in param:
            param[k] = 0
        print("lllll", param)
    for ct_lux in inputdata['Y-Shading']:
        print("ct_lux:", ct_lux)
        if inputdata['Y-Shading'][ct_lux]['0.9F']['current_value'] <= standard:
            outputdata['LNC']['strLsRefLightName']['i32light'][0] = 100
        elif inputdata['Y-Shading'][ct_lux]['0.9F']['current_value'] >= (standard + 0.15):
            outputdata['LNC'][ct_lux]['i32light'][0] = -100
        else:
            outputdata['LNC'][ct_lux]['i32light'][0] = 0
    print("aram11:", param)
    return param


def ColorShadingProcess(inputdata, outputdata):
    # check Y Shading  pass?
    param = outputdata['ALSC']
    print("34567890",outputdata )
    for ct_lux in inputdata['Color-Shading']:
        for RBG in inputdata['Color-Shading'][ct_lux]:
            if inputdata['Color-Shading'][ct_lux][RBG]['current_value'] <= inputdata['Color-Shading'][ct_lux][RBG]['range_min']:
                flag = -1
            elif inputdata['Color-Shading'][ct_lux][RBG]['current_value'] >= inputdata['Color-Shading'][ct_lux][RBG]['range_max']:
                flag = 1
            else:
                flag = 0

            block = RBG.split('_')
            if block[0] == "R":
                param['i8level_r'][0] = 100 * flag
            else:
                param['i8level_b'][0] = 100 * flag
    print("888:", param)
    return param


def LscCheckType(lscinput):
    inputdata = lscinput
    Check_Type = []
    for key in lscinput:
        if key == "Y-Shading":
            for kk in lscinput['Y-Shading']:
                Check_Type.append("Y_Shading")
        elif key == "Color-Shading":
            for ct_lux in lscinput['Color-Shading']:
                #print("ct_lux:", ct_lux, inputdata['Color-Shading'][ct_lux]['R/G Max']['current_value'], inputdata['Color-Shading'][ct_lux]['R/G Min']['current_value'])
                r_g_avg = (inputdata['Color-Shading'][ct_lux]['R/G Max']['current_value'] + inputdata['Color-Shading'][ct_lux]['R/G Min']['current_value']) / 2
                b_g_avg = (inputdata['Color-Shading'][ct_lux]['B/G Max']['current_value'] + inputdata['Color-Shading'][ct_lux]['B/G Min']['current_value']) / 2
                r_g_sub = (inputdata['Color-Shading'][ct_lux]['R/G Max']['current_value'] - inputdata['Color-Shading'][ct_lux]['R/G Min']['current_value']) / 2
                b_g_sub = (inputdata['Color-Shading'][ct_lux]['B/G Max']['current_value'] - inputdata['Color-Shading'][ct_lux]['B/G Min']['current_value']) / 2
                c_v = (inputdata['Color-Shading'][ct_lux]['B/G Max']['range_max'] - inputdata['Color-Shading'][ct_lux]['B/G Min']['range_min']) / 4  #
                print("r-b value:", r_g_avg, b_g_avg, r_g_sub, b_g_sub, "c_v", c_v)
                if r_g_avg < inputdata['Color-Shading'][ct_lux]['B/G Min']['range_min']+0.05 or \
                        r_g_avg > inputdata['Color-Shading'][ct_lux]['B/G Max']['range_max']-0.05 or\
                        b_g_avg < inputdata['Color-Shading'][ct_lux]['B/G Min']['range_min']+0.05 or \
                        b_g_avg > inputdata['Color-Shading'][ct_lux]['B/G Min']['range_max']-0.05:
                    Check_Type.append("AWB")
                elif r_g_sub > c_v or b_g_sub > c_v:
                    Check_Type.append("Color_Shading")
                else:
                    pass

        else:
            pass

    print("Check_Type:", Check_Type)
    return Check_Type

def GetLscData():
    testpath1 = "test_report_tuning.json"
    testpath2 = "sharkL3_param_v0.json"
    inputdata = GetJsonFile(testpath1)
    #inputdata = dict(inputdata['Y-Shading'])
    #inputdata.update(inputdata['Color-Shading'])
    #inputdata = inputdata['Y-Shading'] + inputdata['Color-Shading']
    outputdata = GetJsonFile(testpath2)
    outputdata = outputdata['Common']['LensShading']
    #print("1", type(inputdata), type(outputdata))
    return inputdata, outputdata


def adapt_lsc():
    '''
    log_config()
    logger = logging.getLogger("lsc_main")
    lsc = AtpControl()
    lsc.setFlag(1)
'''
    #logger.info("start lsc !!! \n")
    for k in range(1):
        inputdata, outputdata = GetLscData()
        outputparamweight = LscProcess(inputdata, outputdata)
        # SetOutputParam(outputparamweight)
        f = open("./logs/atp_all.log", 'w+')
        print("-----------\nnum:", k, "\ninputdata:", inputdata, "\noutputdata:", outputdata, "\noutputparamweight:", outputparamweight, "\n")
    #logger.info("end  lsc !!!")


def main():
    '''
    atp = AtpControl()
    while atp.getFlag() == 0:
        break
    #atp.setFlag(0)

    while atp.getFlag() == 0:
        break
    #atp.setFlag(0)
    '''
    adapt_lsc()
    return


if __name__ == "__main__":
    main()
