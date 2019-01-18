#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import os

#set work directory
curPath = os.path.abspath(os.path.dirname(__file__))
sys.path.append(curPath)
os.chdir(curPath)

import logging
from log import log_config
log_config()
logger = logging.getLogger("atp_ctrl")

if __name__ == "__main__":
    logger.info('atp run as main')
else:
    logger.info('atp run as package')
