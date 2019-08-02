from .MotifUtil import MotifUtil
from pprint import pprint as pp


class MEMEUtil:
    def __init__(self, config):
        self.scratch = config['scratch']
        self.MotifUtil = MotifUtil(config)

    # parse output into old motif format(maybe new format if thats useful?)
    def parse(self, outputFile, params):
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

        return self.MotifUtil.parse_motif_list(motifList, params)
