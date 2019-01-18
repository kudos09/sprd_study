import xlrd

def get_xls_data(xlsname):
    dataresultrow = [] # 保存从excel表中读取出来的值，每一行为一个list，dataresult中保存了所有行的内容
    dataresultcol = []
    result = []
    dataresulta = [] # 是由dict组成的list，是将dataresult中的内容全部转成字典组成的list：result

    worksheet = xlrd.open_workbook(xlsname)
    sheet_names = worksheet.sheet_names()
    print("sheet:", sheet_names)
    for sheet_namee in sheet_names:
        table = worksheet.sheet_by_name(sheet_namee)
        result.clear()
        dataresultcol.clear()
        dataresultrow.clear()
        for i in range(0, table.nrows):
            dataresultcol.append(table.cell_value(i, 0))
            for j in range(1, table.ncols):
                dataresultrow.append(table.cell_value(i, j))

        dataresult=[dataresultrow[k:k + j] for k in range(0, len(dataresultrow), j)]
        temp = dict(zip(dataresultcol, dataresult))
        dataresulta.append(temp)
        result.append(dataresulta)
    print("\nresult:\n", result)
    return



if __name__ == '__main__':
    xlsname = "tplm_lsc_ver0000.xlsx"  # excel表的名字
    get_xls_data(xlsname)
    print ("json to excel OK")