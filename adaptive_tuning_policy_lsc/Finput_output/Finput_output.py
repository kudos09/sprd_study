#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import os
import json, xlwt


def GetJsonFile(jsfile):
    f = open(jsfile, encoding='utf-8')
    jsonData = json.load(f)
    # print(jsonData);
    return jsonData


def lscinputdata(jsonData):
    data0 = jsonData['Y-Shading'].items()
    data1 = jsonData['Color-Shading'].items()
    inputdata = {}
    # Y shading
    for key0 in data0:
        data00 = ("Y_lsc." + key0[0]),
        score00 = key0[1]['0.9F'][3],
        Yinputdata = dict(zip(data00, score00))
        inputdata.update(Yinputdata)
        # print("Y-Shading:", Yinputdata)

    # color shading
    for key1 in data1:
        key2 = key1[0]
        data11 = key2,
        data10 = jsonData['Color-Shading'][key2].items()
        for kk in data10:
            data22 = kk[0],
            score11 = kk[1][1],
            data11 = ("C_lsc." + key2 + "." + kk[0]),
            Cinputdata = dict(zip(data11, score11))
            # print("Color-Shading:", data11, Cinputdata)
            inputdata.update(Cinputdata)

    # print(inputdata)
    return inputdata


def lscoutputdata(outputdata):
    # print(outputdata)
    for key1 in outputdata['Common']:
        for key2 in outputdata['Common'][key1]:
            key3 = 0  # outputdata['Common'][key1].items()
            # for key3 in outputdata['Common'][key2]:
            print("11", key1, "22", key2, "33", key3);


def lsctype(lscinput):
    # print(lscinput)
    max_standard = 1.1
    min_satndard = 0.9
    inputdata = lscinput.items()
    # print(inputdata)
    k = 0
    b_g_avg = 9.10  # (inputdata[k+2][1] + inputdata[k+4][1]) / 2
    r_g_avg = 1.1  # (inputdata[k+3][1] + inputdata[k+5][1]) / 2
    b_g_sub = 0.10  # (inputdata[k+2][1] - inputdata[k+4][1]) / 2
    r_g_sub = 0.1  # (inputdata[k+3][1] - inputdata[k+5][1]) / 2
    c_v = (max_standard - min_satndard) / 2  # 0.10000000000000003
    # c_s = (max_standard - min_satndard) / 2
    if r_g_sub >= c_v or b_g_sub >= c_v:
        print("lsc fail", c_v)
    elif r_g_avg <= min_satndard or r_g_avg >= max_standard or b_g_avg <= min_satndard or b_g_avg >= max_standard:
        print("awb fail ")
    else:
        print("eeeeeee")


def main():
    testpath = "./test_report.json"
    parampath = "./board_param.json"
    inputjsondata = GetJsonFile(testpath)
    outputjsondata = GetJsonFile(parampath)
    lscinput = lscinputdata(inputjsondata)
    # lscoutput = lscoutputdata(outputjsondata)
    lsctype(lscinput)


if __name__ == "__main__":
    main()
