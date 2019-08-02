import os
from .MotifUtil import MotifUtil

class HomerUtils:
    def __init__(self, config):
        self.scratch = config['scratch']
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.MotifUtil = MotifUtil(config)

    def parse(self, path, params,
              location_file='homer_locations.txt', motif_file='homerMotifs.all.motifs'):
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

        return self.MotifUtil.parse_motif_list(motifList, params)
