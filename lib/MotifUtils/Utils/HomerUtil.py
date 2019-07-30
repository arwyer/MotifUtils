import sys
import os
import json
import subprocess

from installed_clients.DataFileUtilClient import DataFileUtil


class HomerUtils:
    def __init__(self, config):
        self.scratch = config['scratch']
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.dfu = DataFileUtil(self.callback_url)

    def parse_motif_list(self, motiflist):

    def parse(self, path,location):
        outputFilePath = path
        locationFilePath = location
        homerFile = open(outputFilePath,'r')
        motifList = []
        motifDict = {}
        pwmList = []
        for line in homerFile:
            if '>' in line:
                if len(motifDict) != 0:
                    motifDict['pwm'] = pwmList
                    pwmList = []
                    motifDict['Locations'] = []
                    motifList.append(motifDict)
                    motifDict = {}
                elems = line.split()
                motif = elems[0].replace('>','')
                motifDict['Iupac_signature'] = motif
                p_val = float(elems[5].split(',')[2].split(':')[1])
                motifDict['p-value'] = p_val
            else:
                elems = line.split()
                rowList = []
                rowList.append(('A',float(elems[0])))
                rowList.append(('C',float(elems[1])))
                rowList.append(('G',float(elems[2])))
                rowList.append(('T',float(elems[3])))
                pwmList.append(rowList)

        locationFile = open(locationFilePath,'r')
        for line in locationFile:
            if len(line.split()) == 7:
                elems = line.split()
                motif = elems[0].split('-')[1]
                for m in motifList:
                    if m['Iupac_signature'] == motif:
                        locList = []
                        locList.append(elems[1])
                        locList.append(elems[2])
                        locList.append(elems[3])
                        locList.append(elems[4])
                        m['Locations'].append(locList)
                        break

        return self.parse_motif_list(motifList)
