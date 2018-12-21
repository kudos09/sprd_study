#!/usr/bin/python
# -*- coding: UTF-8 -*-

import threading
import logging

class AtpControl:
    def __init__(self):
        self.__logger = logging.getLogger("atp_main")
        self.__logger.info('AtpControl enter')
        self.__exeFlag = 0

    def __del__(self):
        self.__logger.info('AtpControl exit')

    def setFlag(self, flag):
        self.__logger.debug('__exeFlag=%d',flag)
        if flag == 0:
            return
        self.__exeFlag = flag
        # 开启线程，传入参数
        self.__thread = threading.Thread(target=self.__process)
        self.__thread.setDaemon(True)
        self.__thread.start()  # 启动线程

    def getFlag(self):
        return self.__exeFlag

    def setTestResult(self,msg):
        return

    def setTuningParams(self,msg):
        return

    def getStrategyLibState(self):
        return

    def __process(self):
            self.__logger.debug('processing......')
            self.__exeFlag = 0;





