#!/usr/bin/python3
# -*- coding: UTF-8 -*-
#该代码为子类使用父类参考代码

from tplm_parent import *
import logging
from lsc_data import *
log_tags = "tplm_lsc:\n"

class tplm_lsc(tplm_parent):
    def __init__(self):
        self.__logger = logging.getLogger("atp_tplm")
        tplm_parent.__init__(self, "tplm_lsc")
        self.__logger.info("tplm_lsc start")

    def tplGetSolution(self, tpl_input):
        #print(log_tags, tpl_input)
        outparam = []
        for i in range(len(tpl_input)):
            Fail_data = tpl_input[i]
            if Fail_data[0] == "Y-Shading":
                Fail_Y = Fail_data
                if len(Fail_Y) > 1:
                    pramYoutput = YShadingProcess(Fail_Y, outputdata)
                else:
                    pass
            else:
                Fail_C = Fail_data
                if len(Fail_C) > 1:
                    Type_Lsc, Type_Awb, Type_PG = LscCheckType(Fail_C)
                    # print("Type:\n", Type_Lsc, "\n", Type_Awb)
                    if len(Type_Lsc) > 1:
                        pramCoutput = ColorShadingProcess(Type_Lsc, outputdata)
                    elif len(Type_Awb) > 1:
                        pramawboutput = AwbProcess(Type_Awb)
                    elif len(Type_PG) > 1:
                        prampgoutput = PostGainProcess(Type_Awb)
                    else:
                        pass
        outparam.append(pramYoutput)
        outparam.append(pramCoutput)
        #outparam.append(pramawboutput)
        #outparam.append(prampgoutput)
        print("\n\noutparam:\n", outparam)
        self.__logger.info("tplGetSolution")
        return outparam


def PostGainProcess(Yinputdata, Youtputdata):
    postgain = ["post gain"]
    # print(Yinputdata)
    return postgain


def YShadingProcess(Yinputdata, Youtputdata):
    outputdata = ['Y-Shading_resolution']
    #print("Youtputdata:", Youtputdata)
    for i in range(1, len(Yinputdata), 2):
        if Yinputdata[i + 1]['score'] < 0:
            flag = -1
        else:
            flag = 1

        ct = Yinputdata[i].split('_')
        for j in range(len(Yinputdata)+1):
            #rint("df:", j, Youtputdata[j+1]['strLsRefLightName'],  ct[0])
            if Youtputdata[j+1]['strLsRefLightName'] == ct[0]:
                Youtputdata[j+1]['i32light'] = 100 * flag
    outputdata.append(Yinputdata[i])
    outputdata.append(Youtputdata)
    # print(outputdata)
    return outputdata


def ColorShadingProcess(Cinputdata, Coutputdata):
    outputdata = ['Color-Shading_resolution']
    return outputdata


def AwbProcess(Cinputdata):
    awbdata = ['AwbProcess_report']
    return awbdata


def LscCheckType(inputdata):
    Check_Type_Lsc = []
    Check_Type_Awb = []
    Check_Type_PG = []

    for ct_lux in range(2, len(inputdata), 2):
        # print("ct_lux:", ct_lux, inputdata[ct_lux]['R/G Max']['current_value'])
        r_g_avg = (inputdata[ct_lux]['R/G Max']['current_value'] + inputdata[ct_lux]['R/G Min']['current_value']) / 2
        b_g_avg = (inputdata[ct_lux]['B/G Max']['current_value'] + inputdata[ct_lux]['B/G Min']['current_value']) / 2
        r_g_sub = (inputdata[ct_lux]['R/G Max']['current_value'] - inputdata[ct_lux]['R/G Min']['current_value']) / 2
        b_g_sub = (inputdata[ct_lux]['B/G Max']['current_value'] - inputdata[ct_lux]['B/G Min']['current_value']) / 2
        c_v = (inputdata[ct_lux]['B/G Max']['range_max'] - inputdata[ct_lux]['B/G Min']['range_min']) / 4

        # print("r-b value:", r_g_avg, b_g_avg, r_g_sub, b_g_sub, "c_v", c_v)
        ct = inputdata[ct_lux-1].split('_')
        #print("20lux",ct, inputdata[ct_lux-1])
        if ct[1] == "20lux":
            Check_Type_PG.append("PostGain")
            Check_Type_PG.append(inputdata[ct_lux - 1])
            Check_Type_PG.append(inputdata[ct_lux])
        elif r_g_avg < inputdata[ct_lux]['B/G Min']['range_min'] + 0.05 or \
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

    return Check_Type_Lsc, Check_Type_Awb, Check_Type_PG


if __name__ == "__main__":
    #logging config
    import sys
    import os
    curPath = os.path.abspath(os.path.dirname(__file__))
    rootPath = os.path.split(curPath)[0]
    sys.path.append(rootPath)
    os.chdir(rootPath)
    from log import log_config
    log_config()

    testpath1 = "./tplm/test_report_tuning.json"
    testpath2 = "./tplm/sharkL3_param_v0.json"
    inputdata, outputdata = GetLscData(testpath1, testpath2)
    fail_y, fail_c = GetFail(inputdata)
    print(log_tags, "   inputdata:\n", inputdata, "\n   outputdata:\n", outputdata)
    print(log_tags,  "  Fail_Y:\n", fail_y, "\n   Fail_C:\n", fail_c)
    fail = [fail_y, fail_c]
    #test program
    tp = tplm_lsc()
    tp.tplTraining(123)
    tp.tplGetSolution(fail)


