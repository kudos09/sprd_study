#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import os
import json, xlwt


def GetJsonFile(jsfile):
    f = open(jsfile, encoding='utf-8')
    jsonData = json.load(f)
    return jsonData


def lscinputdata(testpath):
    jsonData = GetJsonFile(testpath)
    data0 = jsonData['Y-Shading'].items()
    data1 = jsonData['Color-Shading'].items()
    inputdata = {}
    # Y shading
    for key0 in data0:
        data00 = ("Y_lsc." + key0[0]),
        score00 = key0[1]['0.9F'],
        Yinputdata = dict(zip(data00, score00))
        inputdata.update(Yinputdata)
        # print("Y-Shading:", Yinputdata)

    # color shading
    for key1 in data1:
        key2 = key1[0]
        data10 = jsonData['Color-Shading'][key2].items()
        for kk in data10:
            score11 = kk[1],
            data11 = ("C_lsc." + key2 + "." + kk[0]),
            Cinputdata = dict(zip(data11, score11))
            inputdata.update(Cinputdata)

    Finputdata = json.dumps(inputdata, indent=4, ensure_ascii=False)
    return Finputdata


def lscoutputdata(parampath):
    jsonoutData = GetJsonFile(parampath)
    # print(jsonoutData)
    outputdata = {}
    value = 0,
    for key1 in jsonoutData['Common']:
        for key2 in jsonoutData['Common'][key1]:
            key1 + key2

    for k in range(len(jsonoutData['Common']['LensShading']['ALSC'])):
        for key3 in jsonoutData['Common']['LensShading']['ALSC']:
            data3 = (key1 + "." + "ALSC" + "." + key3),
            Cinputdata = dict(zip(data3, value))
            outputdata.update(Cinputdata)
    for k in range(len(jsonoutData['Common']['LensShading']['LNC'])):
        for key4 in jsonoutData['Common']['LensShading']['LNC'][k]:
            data4 = (key1 + "." + "LNC" + "." + key4),
            Cinputdata = dict(zip(data4, value))
            outputdata.update(Cinputdata)

    Foutputdata = json.dumps(outputdata, indent=4, ensure_ascii=False)
    return Foutputdata

def main():
    testpath = "test_report_tuning.json"
    parampath = "./sharkL3_param_v0.json"
    inputdata = lscinputdata(testpath)
    outputdata = lscoutputdata(parampath)
    #print("\ninputdata:", inputdata, "\noutputdata:", outputdata)

if __name__ == "__main__":
    main()
