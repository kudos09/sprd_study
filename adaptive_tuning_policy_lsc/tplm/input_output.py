

def GetFail(inputdata):
    fail_Y = ['Y-Shading']
    fail_C = ['Color-Shading']
    for k1 in inputdata['Y-Shading']:
        for k2 in inputdata['Y-Shading'][k1]:
            if inputdata['Y-Shading'][k1][k2]['test_result'] == "FAIL":
                fail_Y.append(k1)
                fail_Y.append(inputdata['Y-Shading'][k1][k2])
                #print("KY", k1, k2, fail_Y)
                break
    for k11 in inputdata['Color-Shading']:
        for k22 in inputdata['Color-Shading'][k11]:
            if inputdata['Color-Shading'][k11][k22]['test_result'] == "FAIL":
                fail_C.append(k11)
                fail_C.append(inputdata['Color-Shading'][k11])
                #print("KC", k11, k22, fail_C)
                break

    return  fail_Y, fail_C



def GetLscData():
    testpath1 = "test_report_tuning.json"
    testpath2 = "sharkL3_param_v0.json"
    inputdata = GetJsonFile(testpath1)
    outputdata = GetJsonFile(testpath2)
    outputdata = outputdata['Common']['LensShading']
    print(inputdata, "\n", outputdata)
    return inputdata, outputdata



