# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 20:01:19 2020

@author: Sivaraman Lakshmipathy
"""

import os
import logging
import datetime

#Custom logger to be used across modules
class logger_handler:
    log_dir = os.path.dirname(os.getcwd()) + os.path.sep + "logs"
    log_level_DEBUG = 'DEBUG'
    log_level_INFO = 'INFO'
    log_level_WARNING = 'WARNING'
    log_level_ERROR = 'ERROR'
    log_level_CRITICAL = 'CRITICAL'

    def __init__(self):
        self.logger = None
        self.setup()

    def setup(self):
        try:
            if not os.path.exists(self.log_dir):
                try:
                    os.mkdir(self.log_dir)
                except Exception as e:
                    print("Error creating logging directory. Logger unavailable.")
                    self.logger = None
                    return
            file_full_path = self.log_dir + os.path.sep + "log_" + str(int(datetime.datetime.now().timestamp())) + ".log"
            logging.basicConfig(filename=file_full_path, format='%(asctime)s %(levelname)s %(message)s')
            self.logger = logging.getLogger()
            self.logger.setLevel(logging.NOTSET)
        except Exception as e:
            print("Error initializing logger. Logger unavailable.", e)
            self.logger = None

    def log_message(self, message, level=None):
        if self.logger is None:
            return

        if level is None:
            level = logger_handler.log_level_INFO

        if level == logger_handler.log_level_CRITICAL:
            self.logger.critical(message)
        elif level == logger_handler.log_level_DEBUG:
            self.logger.debug(message)
        elif level == logger_handler.log_level_ERROR:
            self.logger.error(message)
        elif level == logger_handler.log_level_INFO:
            self.logger.info(message)
        elif level == logger_handler.log_level_WARNING:
            self.logger.warning(message)

class custom_logger:
    logger = logger_handler()

    def log_message(self, message, level=None):
        self.logger.log_message(message, level)
