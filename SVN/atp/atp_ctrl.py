#!/usr/bin/python
# -*- coding: UTF-8 -*-

import logging 

class atp_ctrl:
    def __init__(self):
        self.__logger = logging.getLogger("atp_ctrl")
        self.__logger.info('atp_ctrl init')
    

    def __del__(self):
        return 0
        
    def set_tuning_msg(self,msg):
        self.__msg = msg
        
    def get_tuning_msg(self):
        return self.__msg

    def run_tuning(self):
        return 0;
        
