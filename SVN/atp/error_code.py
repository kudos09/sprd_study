#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
此类库包含错误编码的实现
Owner: Zhongchang.Yang, 2018/12/28
参考网站：
https://www.jb51.net/Special/636.htm
docs.python.org/2/library/json.html
'''
#define the whole of error codes here
error_codes = [
    ["000000","Ok"],
    ["000001","File not Exists"],
    ["000002", "Not implement"],
    ["000003", "Reserved"]
]

def check_error_code(ecode):
    for error_code in error_codes:
        if ecode == error_code[0]:
            return error_code[1]
    return 'Are you kidding? it is not in our error code list!'
