#!/usr/bin/env python
# -*- coding: utf-8 -*-

# CLODv.py: naively versioning CLOD

import rdflib
import os
import logging
import csv
from itertools import combinations
from ConfigParser import SafeConfigParser

CONFIG_INI = "config.ini"

class CLODv:
    def __init__(self, __config):
        self.log = logging.getLogger("CLODv")
        self.config = __config
        self.PATH = self.config.get('general', 'path')
        
        self.parseFiles()

    def parseFiles(self):
        '''
        Parses all combinations of files in the stats dir path
        '''
        for root, dirs, files in os.walk(self.PATH):
            for f in combinations(files, 2):
                self.parsePair(os.path.join(root, f[0]), os.path.join(root, f[1]))

    def parsePair(self, fA, fB):
        '''
        Parses a pair of files in the stats dir
        '''
        currFileA = list(csv.reader(open(fA, 'rb'), delimiter='\t'))
        currFileB = list(csv.reader(open(fB, 'rb'), delimiter='\t'))
        currTotalA = self.sumTotal(currFileA)
        currTotalB = self.sumTotal(currFileB)

    def sumTotal(self, f):
        '''
        Sums the total freqs of stats file f
        '''
        total = 0
        for line in f:
            total += line[1]
        self.log.info("File %s sums total %s" % (f, total))

        
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
