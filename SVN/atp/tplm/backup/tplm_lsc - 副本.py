#!/usr/bin/python3
# -*- coding: UTF-8 -*-
#该代码为子类使用父类参考代码

from tplm_parent import *
import logging
from lsc_data import *
#from lib_lsc import *

from SVN.atp.tplm.lib_lsc import tplm_lsc_process

log_tags = "tplm_lsc:\n"

class tplm_lsc(tplm_parent):
    def __init__(self):
        self.__logger = logging.getLogger("atp_tplm")
        tplm_parent.__init__(self, "tplm_lsc")
        self.__logger.info("tplm_lsc start")
        tplm_lsc_process.__init__(self)

    def tplGetSolution(self, tpl_input, param):
        print(log_tags, tpl_input)
        tpl_input_all = tpl_input
        param_record = [param,]
        test_record = []
        test_data = 0
        flag = 1
        #pramoutput = 0
        tplm_lsc_process_ = tplm_lsc_process()
        while (flag > 0):
            print("flag:", flag)
            if flag == 0:
                check_result = tplm_lsc_process.CheckGoldProcess(tplm_lsc_process_, tpl_input)
                if check_result == 0:
                    print("next case")
                    flag = 1
                    continue
                else:
                    print(" out solution")
                    break
            elif flag == 11:
                return
            else:
                for key in tpl_input:
                    flag = 0
                    if key == 'Y-Shading':
                        test_record.append('Y-Shading')
                        for test_case in tpl_input['Y-Shading']:
                            #print(test_case)
                            test_data = test_case
                            test_record.append(test_case)
                            test_data = test_case
                            print("\n10 Y-Shading:", test_case, tpl_input['Y-Shading'][test_case])
                            pramoutput = tplm_lsc_process.YShadingProcess(tplm_lsc_process_, tpl_input['Y-Shading'][test_case], param)
                            param_record.append(pramoutput)

                            #print("\nparam_record:\n", param_record)
                            self.__logger.info("Y-Shading tplGetSolution")
                            print("\nY-Shading-pramoutput:\n", pramoutput)
                            return pramoutput


                    elif key == 'Color-Shading':
                        test_record.append('Color-Shading')
                        for test_case in tpl_input['Color-Shading']:
                            #print(test_case)
                            test_data = test_case
                            test_record.append(test_case)
                            print("\n11 Color-Shading:", test_case, tpl_input['Color-Shading'][test_case])
                            pramoutput = tplm_lsc_process.ColorShadingProcess(tplm_lsc_process_,tpl_input['Color-Shading'][test_case], param)
                            param_record.append(pramoutput)

                            #print("\nparam_record:\n", param_record)
                            self.__logger.info("Color-Shading tplGetSolution")
                            print("\nColor-Shading-pramoutput:\n", pramoutput)
                            return pramoutput


                    elif key == 'PostGain':
                        test_record.append('PostGain')
                        for test_case in tpl_input['PostGain']:
                            #print(test_case)
                            test_data = test_case
                            test_record.append(test_case)
                            print("\n12 PostGainProcess:\n", test_case, tpl_input['PostGain'][test_case])
                            pramoutput = tplm_lsc_process.PostGainProcess(tplm_lsc_process_, tpl_input['PostGain'][test_case], param)
                            param_record.append(pramoutput)

                            #print("\nparam_record:\n", param_record)
                            self.__logger.info("PostGain tplGetSolution")
                            print("\nPostGain-pramoutput:\n", pramoutput)
                            return pramoutput


                    else:
                        flag = -1


class tplm_lsc_process():


    def __init__(self):
        self.__logger = logging.getLogger("atp_tplm")
        self.__logger.info("tplm_lsc_process start")

    def PostGainProcess(self, Yinputdata, Youtputdata):
        postgain = ["PostGain_resolution"]
        print("\nPostGainProcess:\n", postgain)
        return postgain


    def YShadingProcess(self,Yinputdata, Youtputdata):
        outputdata = ['Y-Shading_resolution']
        #print("Youtputdata:\n", Youtputdata, "\nYinputdata:\n", Yinputdata )
        for i in range(1, len(Yinputdata)):
            if Yinputdata[i + 1]['score'] < 0:
                flag = -1
            else:
                flag = 1

            ct = Yinputdata[i].split('_')
            for j in range(len(Yinputdata)+1):
                #print("df:", j, Youtputdata[j+1]['strLsRefLightName'],  ct[0])
                if Youtputdata[j+1]['strLsRefLightName'] == ct[0]:
                    Youtputdata[j+1]['i32light'] = 100 * flag
        #outputdata.append(Yinputdata[i])
        outputdata.append(Youtputdata)
        print("\nYShadingProcess:\n", outputdata)
        return outputdata


    def ColorShadingProcess(self,Cinputdata, Coutputdata):
        outputdata = ['Color-Shading_resolution']
        print("\nColorShadingProcess:\n", outputdata)
        return outputdata


    def CheckGoldProcess(self,inputdata):
        print("CheckGoldProcess:", inputdata)
        if inputdata['Y-Shading'] == "A_20lux":
            return 0
        else:
            return -1


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
    print(log_tags, "   inputdata:\n", inputdata, "\n   outputdata:\n", outputdata)

    #test program
    tp = tplm_lsc()
    tp.tplTraining(123)
    tp.tplGetSolution(inputdata, outputdata)


