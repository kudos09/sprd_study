#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

class tplm_parent:
    def __init__(self,tpl_id):
        self.tpl_id = tpl_id
        self.__logger = logging.getLogger("atp_tplm")
    def __del__(self):
        return 0

    def tplGetId(self):
        return self.tpl_id

    def tplTraining(self,tpl_dataset):
        self.__logger.info("%s :not support tplTraining",self.tpl_id)

    def tplGetSolution(self,tpl_input):
        self.__logger.info("%s:not support tplGetSolution",self.tpl_id)


