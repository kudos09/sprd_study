#!/usr/bin/python
# -*- coding: UTF-8 -*-

import logging

if __name__ == "__main__":
    # logging config
    import sys
    import os

    curPath = os.path.abspath(os.path.dirname(__file__))
    rootPath = os.path.split(curPath)[0]
    sys.path.append(rootPath)
    os.chdir(rootPath)
    from log import log_config
    log_config()

    logger = logging.getLogger("atp_tplm")
    logger.info('tplm run as main')
else:
    logger = logging.getLogger("atp_tplm")
    logger.info('tplm run as package')
