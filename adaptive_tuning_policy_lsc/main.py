#!/usr/bin/python
# -*- coding: UTF-8 -*-

import logging
from pkgs.atp_main import AtpControl
from log import log_config

def main():
    logger.info('ATP program run')
    atp = AtpControl()

    while atp.getFlag() == 0:
        break
    atp.setFlag(1)

    while atp.getFlag() == 0:
        break
    atp.setFlag(1)

    #adapt_lsc()

    return

if __name__ == "__main__":
    log_config()
    logger = logging.getLogger("atp_main")
    main()
