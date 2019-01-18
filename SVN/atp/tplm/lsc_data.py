#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
import os
import json, xlwt



def GetJsonFile(jsfile):
    #print(os.path.realpath(jsfile))
    f = open(jsfile, encoding='utf-8')
    jsonData = json.load(f)
    #Finputdata = json.dumps(jsonData, indent=4, ensure_ascii=False)
    return jsonData

def GetLscData(testpath1, testpath2):
    FinputdataY = []
    FinputdataC = []
    FinputdataP = []
    FinputdataY.append("Y-Shading")
    FinputdataC.append("Color-Shading")
    FinputdataP.append("PostGain")

    Foutputdata = []
    Foutputdata.append("LensShading.LNC")

    #testpath1 = "./test_report_tuning.json"
    #testpath2 = "./sharkL3_param_v0.json"
    inputdata = GetJsonFile(testpath1)
    outputdata = GetJsonFile(testpath2)
    for kk in inputdata:
        if kk == "Y-Shading":
            for key in inputdata[kk]:
                ct = key.split('_')
                #print("CT:", key, ct)
                if ct[1] == "20lux":
                    FinputdataP.append(key)
                    FinputdataP.append(inputdata[kk][key])
                else:
                    FinputdataY.append(key)
                    FinputdataY.append(inputdata[kk][key])
        elif kk == "Color-Shading":
            for key in inputdata[kk]:
                ct = key.split('_')
                #print("CT:", key, ct)
                if ct[1] == "20lux":
                    FinputdataP.append(key)
                    FinputdataP.append(inputdata[kk][key])
                else:
                    FinputdataC.append(key)
                    FinputdataC.append(inputdata[kk][key])
        else:
            pass
    Finputdata = [FinputdataY, FinputdataC, FinputdataP]
    #Finputdata = dict(FinputdataY)
    #Finputdata.update(FinputdataC)
    #Finputdata.update(FinputdataP)

    for LNC in outputdata['Common']['LensShading']['LNC']:
        Foutputdata.append(LNC)

    Foutputdata.append("LensShading.ALSC")
    ALSC = outputdata['Common']['LensShading']['ALSC']
    Foutputdata.append(ALSC)

    #print("lsc_data:", "\nFinputdata:\n",  Finputdata, "\noutputdata\n", Foutputdata)
    return Finputdata, Foutputdata

def GetFail(inputdata):
    fail_Y = ['Y-Shading']
    fail_C = ['Color-Shading']
    for k1 in inputdata['Y-Shading']:
        for k2 in inputdata['Y-Shading'][k1]:
            if inputdata['Y-Shading'][k1][k2]['test_result'] == "FAIL":
                fail_Y.append(k1)
                fail_Y.append(inputdata['Y-Shading'][k1][k2])
                # print("KY", k1, k2, fail_Y)
                break
    for k11 in inputdata['Color-Shading']:
        for k22 in inputdata['Color-Shading'][k11]:
            if inputdata['Color-Shading'][k11][k22]['test_result'] == "FAIL":
                fail_C.append(k11)
                fail_C.append(inputdata['Color-Shading'][k11])
                # print("KC", k11, k22, fail_C)
                break

    return fail_Y, fail_C

def adapt_lsc():
    testpath1 = "test_report_tuning.json"
    testpath2 = "sharkL3_param_v0.json"
    inputdata, outputdata = GetLscData(testpath1, testpath2)
    print("lsc_data:", "\ninputdata:\n",  inputdata, "\noutputdata\n", outputdata)
    #Fail_Y, Fail_C = GetFail(inputdata)
    #print("lsc_data:",  "\nFail_Y:\n", Fail_Y, "\nFail_C:\n", Fail_C)

def main():
    adapt_lsc()
    return

if __name__ == "__main__":
    main()
