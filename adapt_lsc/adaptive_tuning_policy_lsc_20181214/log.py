#!/usr/bin/python
# -*- coding: UTF-8 -*-

import logging
import logging.config
import logging.handlers
import json
import os

def log_config():
    
    path="./configs/atp_log_cfg.json"
    if os.path.exists(path):
        with open(path, "r", encoding='utf-8') as f:
            f=open(path, "r", encoding='utf-8')
            config = json.load(f)
        logging.config.dictConfig(config)
        ann_logger=logging.getLogger("atp_main")
        ann_logger.info("loading logging config sucess")
    else:
        f_handler = logging.handlers.RotatingFileHandler('./logs/atp_errors.log',)
        f_handler.setLevel(logging.DEBUG)
        f_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))
        ann_logger=logging.getLogger("atp_main")
        ann_logger.setLevel(logging.DEBUG)
        ann_logger.addHandler(f_handler)
        ann_logger.error("configs/atp_log_cfg.json not existed.")
    
    return
