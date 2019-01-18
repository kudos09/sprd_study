#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import logging

class tplm_lsc_process:
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





