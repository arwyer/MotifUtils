import sys
import os
import json
import subprocess
from copy import deepcopy

from installed_clients.DataFileUtilClient import DataFileUtil


class HomerUtils:
    def __init__(self, config):
        self.scratch = config['scratch']
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.dfu = DataFileUtil(self.callback_url)

    def parse_motif_list(self, motiflist):
        MSO = {}
        MSO['Condition'] = 'Temp'
        MSO['SequenceSet_ref'] = '123'
        MSO['Motifs'] = []
        MSO['Alphabet'] = ['A', 'C', 'G', 'T']
        MSO['Background'] = {}
        for letter in MSO['Alphabet']:
            MSO['Background'][letter] = 0.0

        for motif in motiflist:
            MSO['Motifs'].append(deepcopy(self.ConvertMotif(motif, MSO)))

        return MSO

    def ConvertMotif(self, motif, MotifSet):
        newMotif = {}
        newMotif['Motif_Locations'] = []
        SeqDict = {}
        for loc in motif['Locations']:
            new_loc = {}
            # new_loc['Feature_id'] = loc[0]
            new_loc['sequence_id'] = loc[0]
            new_loc['start'] = int(loc[1])
            new_loc['end'] = int(loc[2])
            new_loc['orientation'] = loc[3]
            # new_loc['sequence'] = self.ExtractSequence(int(loc[1]), int(loc[2]), loc[3], loc[0], SeqDict)
            new_loc['sequence'] = ''
            newMotif['Motif_Locations'].append(new_loc.copy())
        newMotif['Iupac_sequence'] = motif['Iupac_signature']
        newMotif['PWM'] = {}
        newMotif['PFM'] = {}

        for letter in MotifSet['Alphabet']:
            newMotif['PWM'][letter] = []
            newMotif['PFM'][letter] = []
        if len(motif['pwm']) != len(motif['Iupac_signature']):
            print('LENGTH MISMATCH ORIGINAL')
        for row in motif['pwm']:
            for pair in row:
                newMotif['PWM'][pair[0]].append(pair[1])
        if len(newMotif['PWM']['A']) != len(newMotif['Iupac_sequence']):
            print('LENGTH MISMATCH NEW')

        return newMotif

    def ExtractSequence(self, start, end, orientation, id, SeqDict):
        complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A', 'N': 'N'}
        if orientation == '+':
            print(id)
            print(SeqDict[id])
            return SeqDict[id][start:end]
        else:
            tempseq = SeqDict[id][start:end]
            newSeq = ''
            for b in tempseq:
                newSeq += complement[b]
            newSeq = newSeq[::-1]
            return newSeq

        pass

    def parse(self, path, location_file='homer_locations.txt', motif_file='homerMotifs.all.motifs'):
        homer_file = os.path.join(path, motif_file)
        location = os.path.join(path, location_file)

        homerFile = open(homer_file,'r')
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

        locationFile = open(location,'r')
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
