import logging
import os
from urllib import request, parse

from installed_clients.DataFileUtilClient import DataFileUtil


class MotifParser:
    def __init__(self, callback, scratch):
        self.scratch = scratch
        self.dfu = DataFileUtil(callback)

        logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                            level=logging.INFO)

    def parseMotif(self, file, motifformat):
        # remove empty keys from file
        removekeys = []
        for k, v in file.items():
            if v == '' or v is None or v == 'NA':
                removekeys.append(k)

        for k in removekeys:
            file.pop(k)

        if not len(file) == 1:
            raise ValueError('Please input a single file location within the parameters:\n' +
                                'file = {\n' +
                                '\t\'shock_id\': \'SHOCKID\',\n' +
                                '\t\'ftp_url\': \'FTPURL\',\n' +
                                '\t\'path\': \'CONTAINERFILEPATH\'\n' +
                                '}\n\n')

        if 'shock_id' in file:
            self.dfu.shock_to_file({
                'shock_id': file['shock_id'],
                'handle_id': '',
                'file_path': os.path.join(self.scratch, 'motifoutput.txt')
            })
            self.motif_file = os.path.join(self.scratch, 'motifoutput.txt')
        elif 'ftp_url' in file:
            try:
                parse.urlparse(file['ftp_url'])
            except Exception:
                raise ValueError('Input parameter motif file is specified as an ftp-url with an' +
                                    'invalid url: ' + str(file['ftp_url']))

            request.urlretrieve(file['ftp_url'], os.path.join(self.scratch, 'motifoutput.txt'))
            self.motif_file = os.path.join(self.scratch, 'motifoutput.txt')
        elif 'path' in file:
            if not os.path.exists(file['path']):
                raise ValueError('The file specified from the input parameter file, does not exists')
            else:
                self.motif_file = file['path']

        formats = ["MEME", "JASPAR", "GIBBS", "HOMER", "TRANSFAC", "MFMD"]

        if motifformat in formats:
            if motifformat == "MEME":
                motifs = self.parseMEMEOutput(self.motif_file)
            else:
                raise ValueError('Only MEME format is supported currently')
        else:
            raise ValueError('Motif format must be: "MEME", "JASPAR", "GIBBS", "HOMER", "TRANSFAC", or "MFMD"')

        MSO = {}
        MSO['Condition'] = 'Temp'
        MSO['FeatureSet_ref'] = '123'
        MSO['Motifs'] = motifs
        MSO['Alphabet'] = ['A', 'C', 'G', 'T']
        MSO['Background'] = {}
        for letter in MSO['Alphabet']:
            MSO['Background'][letter] = 0.0

        return MSO

    def parseMEMEOutput(self, path):
        outputFile = path
        file = open(outputFile, 'r')

        starCount, findLocs, findPWM = 0, 0, 0
        countStars, readMotif, processMotif = False, False, False
        motifDict, motifList = {}, []
        for line in file:
            if 'COMMAND LINE SUMMARY' in line:
                countStars = True
                continue
            if 'SUMMARY OF MOTIFS' in line:
                break
            if countStars:
                if '*****************************************************************' in line:
                    starCount += 1
            if starCount != 0 and starCount % 3 == 0 and not readMotif:
                # new motif
                if starCount != 3:
                    motifList.append(motifDict)
                    motifDict = {}
                    # add the motif we finished
                readMotif = True
                continue
            if readMotif is True:
                elems = line.replace('\n', '').split()
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
                    # strand id = elems[0]
                    locList = []
                    locList.append(elems[0])
                    locList.append(elems[2])
                    if elems[1] == '+':
                        end = str(int(elems[2]) + len(motifSignature))
                    else:
                        end = str(int(elems[2]) - len(motifSignature))
                    locList.append(end)
                    locList.append(elems[1])
                    motifDict['Locations'].append(locList)
                    # orientation = elems[1] +/-
                    # start = elems[2]
                    # no stop, just use width of motif (len motifSignature)
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
                    elems = line.replace('\n', '').split()
                    rowList = []
                    rowList.append(('A', float(elems[0])))
                    rowList.append(('C', float(elems[1])))
                    rowList.append(('G', float(elems[2])))
                    rowList.append(('T', float(elems[3])))
                    motifDict['pwm'].append(rowList)

        return motifList

