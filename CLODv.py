#!/usr/bin/env python
# -*- coding: utf-8 -*-

# CLODv.py: naively versioning CLOD

import rdflib
import os
import logging
import csv
import distance
import json
from itertools import combinations
from ConfigParser import SafeConfigParser

CONFIG_INI = "config.ini"

class CLODv:
    versions = {}

    def __init__(self, __config):
        self.log = logging.getLogger("CLODv")
        self.config = __config
        self.PATH = self.config.get('general', 'path')

        self.log.info("Parsing doc combinations...")
        self.parseFiles()

        self.log.info("Serializing...")
        self.serializeVersions()

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
        if self.areVersions(currFileA, currFileB):
            self.addVersion(fA, fB)
            self.addVersion(fB, fA)

    def addVersion(self, a, b):
        '''
        Adds file b as a version of a
        '''
        if a not in self.versions:
            self.versions[a] = []
        self.versions[a].append(b)

    def areVersions(self, a, b):
        '''
        Decides if a and b are versions of each other
        '''
        return self.similarNamespaces(a, b) and self.similarFrequencies(a, b)

    def similarNamespaces(self, a, b):
        '''
        Decides if a and b have similar namespaces
        '''
        nsA = [line[0] for line in a]
        nsB = [line[0] for line in b]
        return distance.jaccard(nsA, nsB) >= self.config.get('similarity', 'ns')

    def similarFrequences(self, a, b):
        '''
        Decides if a and b have similar namespace frequency
        '''
        freqA = [line[1] for line in a]
        freqB = [line[1] for line in b]
        return distance.jaccard(freqA, freqB) >= self.config.get('similarity', 'freq')
        
    def sumTotal(self, f):
        '''
        Sums the total freqs of stats file f
        '''
        total = 0
        for line in f:
            total += int(line[1])
        return total

    def serializeVersions(self):
        '''
        Serializes versions in a json file
        '''
        with open(self.config.get('general', 'dump'), 'wb') as fp:
            json.dump(self.versions, fp)
        
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
