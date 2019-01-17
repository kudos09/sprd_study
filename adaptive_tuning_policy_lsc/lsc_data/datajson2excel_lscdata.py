# -*- coding: utf-8 -*-
# 这段代码主要的功能是把utf-8格式的json文件转换成excel表格
import json, xlwt
import sys

def writeToExcel(jsonfile,excfile):
    with open(jsonfile, encoding='utf-8') as f:
        jsonData = json.load(f)
    book = xlwt.Workbook()  # 创建excel文件
    style = xlwt.XFStyle()  # 格式信息
    font = xlwt.Font()  # 字体基本设置
    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_CENTER  # May be: HORZ_GENERAL, HORZ_LEFT, HORZ_CENTER, HORZ_RIGHT, HORZ_FILLED, HORZ_JUSTIFIED, HORZ_CENTER_ACROSS_SEL, HORZ_DISTRIBUTED
    alignment.vert = xlwt.Alignment.VERT_CENTER  # May be: VERT_TOP, VERT_CENTER, VERT_BOTTOM, VERT_JUSTIFIED, VERT_DISTRIBUTED
    style.alignment = alignment  # Add Alignment to Style
    font.bold = True
    style.font = font
    dataname = "lsc_data"
    #for k in range(len(jsonData['labell']):
    k = 1
    dataname = dataname + k
    sheet1 = book.add_sheet("策略库输入参数", cell_overwrite_ok=True)  # 创建list表
    sheet2 = book.add_sheet("策略库输出参数", cell_overwrite_ok=True)  # 创建list表

    for testlabel in range(len(jsonData['labell'])):
        sheet1.write(testlabel, 0, testlabel)  # 存入list sheet label
        sheet1.write(testlabel, 1, jsonData['labell'][testlabel])  # 存入list sheet label

        sheet = book.add_sheet(jsonData['labell'][testlabel], cell_overwrite_ok=True)  # 创建labell表
        for titlelen in range(len(jsonData['titall'])):
            sheet.write(0, titlelen, jsonData['titall'][titlelen],style)  # 存入第一行标题
            datanum = 1
            for datalinenum in range(len(jsonData['datashading'])):
                if jsonData['labell'][testlabel] == jsonData['datashading'][datalinenum][0]:   # 匹配对应文件
                    for datalens in range(len(jsonData['datashading'][datalinenum])):
                        #for num in range(len(str(jsonData['datashading'][datalinenum][datalens])))
                        #print("aa",jsonData['datashading'][1][datalens], len(str(jsonData['datashading'][datalinenum][datalens])))
                        if (len(str(jsonData['datashading'][datalinenum][datalens]))) > 10:
                            sheet.col(datalens).width = 256 * (len(str(jsonData['datashading'][datalinenum][datalens]))+2)
                            sheet.write(datanum, datalens, jsonData['datashading'][datalinenum][datalens])  # 匹配对应行写入表
                        else:
                            sheet.col(titlelen).width = 256 * 10
                            sheet.write(datanum, datalens, jsonData['datashading'][datalinenum][datalens])  # 匹配对应行写入表
                        #sheet.write(datanum, datalens, jsonData['datashading'][datalinenum][datalens])  # 匹配对应行写入表
                        #print("datanum:", datanum, "testlabel: ", testlabel, "titlelen: ", titlelen,"datalens: ",datalens,"datalinenum:", datalinenum, jsonData['datashading'][datalinenum])
                    datanum += 1
            book.save(excfile)
    #print(    "Create ", excfile, " OK")


if __name__ == '__main__':
    jsfile = "./data.json"
    excfile = "./data.xls"
    writeToExcel(jsfile, excfile)
print ("json to excel OK")