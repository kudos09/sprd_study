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
    #testpath1 = "./test_report_tuning.json"
    #testpath2 = "./sharkL3_param_v0.json"
    inputdata = GetJsonFile(testpath1)
    outputdata = GetJsonFile(testpath2)
    Foutputdata = []
    Foutputdata.append("Y-Shading")
    for LNC in outputdata['Common']['LensShading']['LNC']:
        for key in LNC:
            if key == "strLsRefLightName":
                pass
            else:
                LNC[key] = 0
        Foutputdata.append(LNC)

    Foutputdata.append("Color-Shading")
    ALSC = outputdata['Common']['LensShading']['ALSC']
    for k in ALSC:
        ALSC[k] = 0
    Foutputdata.append(ALSC)
    #print("lsc_data:", "inputdata:\n",  inputdata, "\noutputdata\n", Foutputdata)
    return inputdata, Foutputdata

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
    #print("lsc_data:", "inputdata:\n",  inputdata, "outputdata\n", outputdata)
    Fail_Y, Fail_C = GetFail(inputdata)
    #print("lsc_data:",  "Fail_Y:\n", Fail_Y, "Fail_C:\n", Fail_C)

def main():
    adapt_lsc()
    return

if __name__ == "__main__":
    main()
