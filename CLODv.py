#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# CLODv.py: naively versioning CLOD

import rdflib
import os
import logging
from ConfigParser import SafeConfigParser

CONFIG_INI = "config.ini"

class CLODv:
    def __init__(self, __config):
        self.log = logging.getLogger("CLODv")
        self.config = __config
        self.PATH = self.config.get('general', 'path')
        
if __name__ == "__main__":
    # Config
    config = SafeConfigParser()
    config.read(CONFIG_INI)
    
    # Logging
    logLevel = logging.INFO
    if config.get('general', 'verbose') == 1:
        logLevel = logging.DEBUG
    logging.basicConfig(level=logLevel)
    logging.info("Initializing...")

    # Instance
    l = CLODv(config)
    logging.info("Exiting...")
    exit(0)
