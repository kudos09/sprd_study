#!/usr/bin/python3
# -*- coding: UTF-8 -*-
#该代码为子类使用父类参考代码

import sys
import os
import json, xlwt
import logging
from log import log_config
from tplm_parent import *
#from lsc_data import *

log_tags = "tplm_lsc:\n"


class tplm_lsc_ver0000(tplm_parent):


    def __init__(self):
        self.__logger = logging.getLogger("atp_tplm")
        tplm_parent.__init__(self, "tplm_lsc")
        self.__logger.info("tplm_lsc start")
        tplm_lsc_process.__init__(self)

    def tplGetSolution(self, tpl_input):
        #print(log_tags, tpl_input)
        global flags, tinning_param
        tpl_input_all = tpl_input
        for key in tpl_input:
            if key == "pre_check":
                pre_check = tpl_input[key]
            elif key == "test_result":
                test_result = tpl_input[key]
            elif key == "tpl_param":
                tpl_param = tpl_input[key]
            elif key == "tinning_param":
                tinning_param = tpl_input[key]
            elif key == "flag":
                flags = tpl_input[key]
            else:
                pass

        param_record = tinning_param
        test_order = tpl_param['Common_LensShading_Tuning_order']
        test_id = len(test_order)
        test_record = []
        flag = flags['option']
        print("\nparam_record\n", param_record, "\ntest_order\n", test_order, test_id, flags)

        tplm_lsc_process_ = tplm_lsc_process()

        checkresult = tplm_lsc_process.PreCheckData(pre_check)
        if checkresult == 0:
            print("pass")
            pass
        else:
            print("fail")
            return checkresult

        while(flag >= 0):
            if flag == 0:
                print("flag:", flag)
                for k in range(len(tpl_input)):
                    for kk in range(1, len(tpl_input[k]), 2):
                        #print("11111:", kk, k, tpl_input[k][0], tpl_input[k][kk], test_data[test_id])
                        if tpl_input[k][0] == 'Y-Shading':
                            test_record.append('Y-Shading')
                            #print(test_data[test_id], "=====", tpl_input[k][kk])
                            if test_data[test_id] == tpl_input[k][kk]:
                                test_record.append(test_data[test_id])
                                ys = [test_data[test_id], tpl_input[k][kk+1]['0.9F']]
                                print("\n10 Y-Shading:", test_data[test_id], tpl_input[k][kk+1]['0.9F'])
                                pramoutput = tplm_lsc_process.YShadingProcess(tplm_lsc_process_, ys, tinning_param)
                                param_record.append(pramoutput)

                                #print("\nparam_record:\n", param_record)
                                self.__logger.info("Y-Shading tplGetSolution")
                                print("\nY-Shading pramoutput:\n", pramoutput)
                                flag = 1
                                #return pramoutput
                                continue

                        elif tpl_input[k][0] == 'Color-Shading':
                            test_record.append('Color-Shading')
                            #print(test_data[test_id, "=====", tpl_input[k][kk])
                            if test_data[test_id] == tpl_input[k][kk]:
                                test_record.append(test_data[test_id])
                                cs = [test_data[test_id], tpl_input[k][kk+1]]
                                print("\n11 Color-Shading:", test_data[test_id], tpl_input[k][kk+1])
                                pramoutput = tplm_lsc_process.ColorShadingProcess(tplm_lsc_process_, cs, tinning_param)
                                param_record.append(pramoutput)
                                #print("\nparam_record:\n", param_record)
                                self.__logger.info("Color-Shading tplGetSolution")
                                print("\nColor-Shading pramoutput:\n", pramoutput)
                                flag = 1
                                #return pramoutput
                                continue

                        elif tpl_input[k][0] == 'PostGain':
                            test_record.append('PostGain')
                            #print(test_data[test_id], "=====", tpl_input[k][kk])
                            if test_data[test_id] == tpl_input[k][kk]:
                                test_record.append(test_data[test_id])
                                gp = [test_data[test_id], tpl_input[k][kk + 1]]
                                print("\n12 PostGain:", test_data[test_id], tpl_input[k][kk + 1])
                                pramoutput = tplm_lsc_process.PostGainProcess(tplm_lsc_process_, gp, tinning_param)
                                param_record.append(pramoutput)

                                #print("\nparam_record:\n", param_record)
                                self.__logger.info("PostGain tplGetSolution")
                                print("\nPostGain pramoutput:\n", pramoutput)
                                flag = 1
                                #return pramoutput
                                continue
                        else:
                            return  "error"

            elif flag == 1:
                print("flag:", flag)
                check_result = tplm_lsc_process.CheckGoldProcess(tplm_lsc_process_, test_result, tpl_param)
                if check_result == 1:
                    print("CheckGoldProcess：next case")
                    test_id = test_id + 1
                    flag = 0
                    continue
                else:
                    flag = 0
                    print("CheckGoldProcess： out solution")
                    #break
            elif flag == 2:
                print("flag:", flag)
            elif flag == 3:
                print("flag:", flag)
            elif flag == 4:
                print("flag:", flag)
            else:
                print("flag error:", flag)



class tplm_lsc_process(object):


    def __init__(self):
        self.__logger = logging.getLogger("atp_tplm")
        self.__logger.info("tplm_lsc_process start")

    def PreCheckData(pre_check):
        return 0

    def PostGainProcess(self, Yinputdata, Youtputdata):
        postgain = ["PostGain_resolution"]
        print("\nPostGainProcess:\n", postgain)
        return postgain

    def YShadingProcess(self,YSinputdata, YSoutputdata):
        Yinputdata = YSinputdata.copy()
        Youtputdata = YSoutputdata
        outputdata = ['Y-Shading_resolution']
        #print("Youtputdata:\n", Youtputdata, "\nYinputdata:\n", Yinputdata )
        if Yinputdata[1]['score'] < 0:
            flag = -1
        else:
            flag = 1

        ct = Yinputdata[0].split('_')
        for j in range(1, 7):
            #print("2222", j,  Youtputdata[j]['strLsRefLightName'], ct[0])
            if Youtputdata[j]['strLsRefLightName'] == ct[0]:
                Youtputdata[j]['i32light'][0] = 100 * flag
                #print(Youtputdata)
        outputdata.append(Youtputdata)
        print("\nYShadingProcess:\n", "outputdata")
        return outputdata

    def ColorShadingProcess(self,Cinputdata, Coutputdata):
        outputdata = ['Color-Shading_resolution']
        print("\nColorShadingProcess:\n", outputdata)
        return outputdata

    def CheckGoldProcess(self, test_result, tpl_param):
        #print("CheckGoldProcess:", test_result)
        if len(test_result) == 0:
            return 1
        else:
            return 0

def GetLscData(jsfile):
    #print(os.path.realpath(jsfile))
    f = open(jsfile, encoding='utf-8')
    jsonData = json.load(f)
    #Finputdata = json.dumps(jsonData, indent=4, ensure_ascii=False)
    return jsonData

if __name__ == "__main__":
    #logging config
    curPath = os.path.abspath(os.path.dirname(__file__))
    rootPath = os.path.split(curPath)[0]
    sys.path.append(rootPath)
    os.chdir(rootPath)
    log_config()

    testpath = "./tplm/inputdata.json"
    inputdata = GetLscData(testpath)
    print(log_tags, "   inputdata:\n", inputdata)

    #test program
    tp = tplm_lsc_ver0000()
    tp.tplTraining(123)
    tp.tplGetSolution(inputdata)


