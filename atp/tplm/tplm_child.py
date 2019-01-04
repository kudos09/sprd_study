#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#该代码为子类使用父类参考代码
from tplm_parent import *
import logging

class tplm_child(tplm_parent):
    def __init__(self):
        self.__logger = logging.getLogger("atp_tplm")
        tplm_parent.__init__(self,"tplm_child")
        self.__logger.info("tplm_child start")

    def tplGetSolution(self,tpl_input):
        self.__logger.info("tplGetSolution")

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

    #test program
    tp = tplm_child()
    tp.tplTraining(123)
    tp.tplGetSolution("test class function")


