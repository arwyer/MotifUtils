import sys
import os
import json
import subprocess


class MEMEUtil:
    def __init__(self, config):
        self.scratch = config['scratch']

    # build the command to run meme, use some default flags
    def build_meme_command(self, inputFilePath):
        outputFlag = ' -o /kb/module/work/tmp/meme_out -revcomp -dna'
        command = '/kb/deployment/bin/meme/bin/meme ' + inputFilePath + outputFlag

        return command

    # wrapper to subprocess run for now, error check later
    def run_meme_command(self, command):
        try:
            meme_out_txt = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            #print('************PRINTING MEME************\n'+meme_out_txt)
            return meme_out_txt
        except subprocess.CalledProcessError as e:
            print('************MEME ERROR************\n')
            print(e.returncode)
            raise subprocess.CalledProcessError(e)

    # parse output into old motif format(maybe new format if thats useful?)
    def parse_meme_output(self, outputFile):
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
        return motifList
