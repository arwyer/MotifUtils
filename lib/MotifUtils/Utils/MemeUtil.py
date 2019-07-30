import sys
import os
import json
import subprocess
from copy import deepcopy


class MEMEUtil:
    def __init__(self, config):
        self.scratch = config['scratch']

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

    # parse output into old motif format(maybe new format if thats useful?)
    def parse(self, outputFile):
        file = open(outputFile,'r')

        starCount = 0
        countStars = False
        readMotif = False
        processMotif = False
        findLocs = 0
        findPWM = 0
        motifDict = {}
        motifList = []
        for line in file:
            if 'COMMAND LINE SUMMARY' in line:
                countStars = True
                continue
            if 'SUMMARY OF MOTIFS' in line:
                break
            if countStars:
                if '*****************************************************************' in line:
                    starCount += 1
            if starCount != 0 and starCount%3 == 0 and not readMotif:
                #new motif
                if starCount != 3:
                    motifList.append(motifDict)
                    motifDict = {}
                    #add the motif we finished
                readMotif = True
                continue
            if readMotif is True:
                elems = line.replace('\n','').split()
                #print(line)
                motifSignature = elems[1]
                motifDict['Iupac_signature'] = motifSignature
                eval = float(elems[-1])
                motifDict['p-value'] = eval
                motifDict['Locations'] = []
                motifDict['pwm'] = []
                readMotif = False
                processMotif = True
                continue
            if processMotif is True:
                if 'sites sorted by' in line:
                    findLocs = 1
                    continue
                if findLocs == 4:
                    if '-----------------------------' in line:
                        findLocs = 0
                        continue
                    elems = line.replace('\n', '').split()
                    locList = []
                    locList.append(elems[0])
                    locList.append(elems[2])
                    if elems[1] == '+':
                        end = str(int(elems[2])+len(motifSignature))
                    else:
                        end = str(int(elems[2])-len(motifSignature))
                    locList.append(end)
                    locList.append(elems[1])
                    motifDict['Locations'].append(locList)
                    continue
                if findLocs != 0:
                    findLocs += 1
                    continue
                if 'letter-probability matrix' in line:
                    findPWM = 1
                    continue
                if findPWM == 1:
                    if '--------' in line:
                        findPWM = 0
                        continue
                    elems = line.replace('\n','').split()
                    rowList = []
                    rowList.append(('A',float(elems[0])))
                    rowList.append(('C',float(elems[1])))
                    rowList.append(('G',float(elems[2])))
                    rowList.append(('T',float(elems[3])))
                    motifDict['pwm'].append(rowList)

        return self.parse_motif_list(motifList)
