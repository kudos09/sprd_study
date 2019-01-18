#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
import os
import json, xlwt


def GetJsonFile(jsfile):
    f = open(jsfile, encoding='utf-8')
    jsonData = json.load(f)
    # Finputdata = json.dumps(jsonData, indent=4, ensure_ascii=False)
    return jsonData


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


def PostGain(Yinputdata, Youtputdata):
    postgain = ["post gain"]
    #print("post gain !")
    return postgain


def YShadingProcess(Yinputdata, Youtputdata):
    outputdata = ['Y-Shading']
    #print("Yinputdata:", Yinputdata)
    for i in range(1, len(Yinputdata), 2):
        for j in Youtputdata['LNC']:
            ct = Yinputdata[i].split('_')
            # print("CT:", ct, "===?", j['strLsRefLightName'])
            if ct[0] == j['strLsRefLightName']:
                if ct[1] == "20lux":
                    PostGaindat = PostGain(Yinputdata, Youtputdata)
                    outputdata.append(Yinputdata[i])
                    outputdata.append(PostGaindat)
                else:
                    for nn in j:
                        if Yinputdata[i+1]['score'] < 0:
                            flag = -1
                        else:
                            flag = 1
                        #print("flag: ", flag)
                        if nn == "strLsRefLightName":
                            pass
                        else:
                            j[nn] = 0
                    j['i32light'] = 100 * flag
                    outputdata.append(Yinputdata[i])
                    outputdata.append(j)
    #print(outputdata)
    return outputdata


def ColorShadingProcess(Cinputdata, Coutputdata):
    outputdata = ['Color-Shading']
    return outputdata


def AwbProcess(Cinputdata):
    awbdata = ['AwbProcess']
    return awbdata


def LscCheckType(inputdata):
    Check_Type_Lsc = []
    Check_Type_Awb = []
    
    for ct_lux in range(2, len(inputdata), 2):
        # print("ct_lux:", ct_lux, inputdata[ct_lux]['R/G Max']['current_value'])
        r_g_avg = (inputdata[ct_lux]['R/G Max']['current_value'] + inputdata[ct_lux]['R/G Min']['current_value']) / 2
        b_g_avg = (inputdata[ct_lux]['B/G Max']['current_value'] + inputdata[ct_lux]['B/G Min']['current_value']) / 2
        r_g_sub = (inputdata[ct_lux]['R/G Max']['current_value'] - inputdata[ct_lux]['R/G Min']['current_value']) / 2
        b_g_sub = (inputdata[ct_lux]['B/G Max']['current_value'] - inputdata[ct_lux]['B/G Min']['current_value']) / 2
        c_v = (inputdata[ct_lux]['B/G Max']['range_max'] - inputdata[ct_lux]['B/G Min']['range_min']) / 4

        #print("r-b value:", r_g_avg, b_g_avg, r_g_sub, b_g_sub, "c_v", c_v)

        if r_g_avg < inputdata[ct_lux]['B/G Min']['range_min'] + 0.05 or \
                r_g_avg > inputdata[ct_lux]['B/G Max']['range_max'] - 0.05 or \
                b_g_avg < inputdata[ct_lux]['B/G Min']['range_min'] + 0.05 or \
                b_g_avg > inputdata[ct_lux]['B/G Min']['range_max'] - 0.05:
            Check_Type_Awb.append("AWB")
            Check_Type_Awb.append(inputdata[ct_lux - 1])
            Check_Type_Awb.append(inputdata[ct_lux])
        elif r_g_sub > c_v or b_g_sub > c_v:
            Check_Type_Lsc.append("Color_Shading")
            Check_Type_Lsc.append(inputdata[ct_lux - 1])
            Check_Type_Lsc.append(inputdata[ct_lux])
        else:
            pass
        # print("Type:\n", Check_Type_Lsc, "\n", Check_Type_Awb)

    return Check_Type_Lsc, Check_Type_Awb


def GetLscData():
    testpath1 = "test_report_tuning.json"
    testpath2 = "sharkL3_param_v0.json"
    inputdata = GetJsonFile(testpath1)
    outputdata = GetJsonFile(testpath2)
    outputdata = outputdata['Common']['LensShading']
    # print(inputdata, "\n", outputdata)
    return inputdata, outputdata


def adapt_lsc():
    outparam = []
    inputdata, outputdata = GetLscData()
    print("inputdata:\n", inputdata, "\noutputdata:\n", outputdata)
    Fail_Y, Fail_C = GetFail(inputdata)
    # print("Fail_final", len(Fail_Y), Fail_Y, "\n", len(Fail_C), Fail_C)
    if len(Fail_Y) > 1:
        pramYoutput = YShadingProcess(Fail_Y, outputdata)
    else:
        pass

    if len(Fail_C) > 1:
        Type_Lsc, Type_Awb = LscCheckType(Fail_C)
        #print("Type:\n", Type_Lsc, "\n", Type_Awb)
        if len(Type_Lsc) > 1:
            pramCoutput = ColorShadingProcess(Type_Lsc, outputdata)
        elif len(Type_Awb) > 1:
            pramawboutput = AwbProcess(Type_Awb)
        else:
            pass

    else:
        pass
    outparam.append(pramYoutput)
    outparam.append(pramCoutput)
    #outparam.append(pramawboutput)
    print("\n\noutparam:\n", outparam)
    return outparam


def main():
    print("\n - - - - start LSC process - - - - \n")
    adapt_lsc()
    print("\n - - - -  enf LSC process - - - - \n")

if __name__ == "__main__":
    main()
