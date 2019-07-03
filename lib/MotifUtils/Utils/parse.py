import logging
import os
from pprint import pprint as pp
from urllib import request, parse

from .GibbsUtil import GibbsUtil as Gibbs
from .HomerUtil import HomerUtils as Homer
from .MemeUtil import MEMEUtil as MEME
from .MFMDUtil import MFMDUtil as MFMD

from installed_clients.DataFileUtilClient import DataFileUtil


class MotifParser:
    def __init__(self, config):
        self.scratch = config['scratch']
        self.dfu = DataFileUtil(os.environ['SDK_CALLBACK_URL'])

        self.Homer = Homer(config)
        self.Gibbs = Gibbs(config)
        self.MEME = MEME(config)
        self.MFMD = MFMD(config)

        logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                            level=logging.INFO)

    def get_motif_format(self, format):
        supported_formats = {
            "MEME": self.MEME,
            "JASPAR": None,
            "GIBBS": self.Gibbs,
            "HOMER": self.Homer,
            "TRANSFAC": None,
            "MFMD": self.MFMD,
        }

        return supported_formats[format]

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
            # TODO: verify this works with directories and compressed files
            mfile = self.dfu.shock_to_file({
                'shock_id': file['shock_id'],
                'handle_id': '',
                'file_path': self.scratch
            })
            self.motif_file = mfile['path']
        elif 'ftp_url' in file:
            # TODO: verify this works with directories and compressed files
            try:
                parse.urlparse(file['ftp_url'])
            except Exception:
                raise ValueError('Input parameter motif file is specified as an ftp-url with an' +
                                    'invalid url: ' + str(file['ftp_url']))

            self.motif_file = request.urlretrieve(file['ftp_url'], self.scratch)[0]
        elif 'path' in file:
            if not os.path.exists(file['path']):
                raise ValueError('The file specified from the input parameter file, does not exists')
            else:
                self.motif_file = file['path']

        motifinfo = self.get_motif_format(motifformat)

        if motifinfo is None:
            raise NotImplementedError(f'Motif format ({motifformat}) is not supported yet')

        MSO = motifinfo.parse(file)

        return MSO
    """
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

    def parseHOMEROutput(self, homer_output_dir):
        if not os.path.isdir(homer_output_dir):

        motif_file = os.path.join(homer_output_dir, 'homerMotifs.all.motifs')

        if not os.path.exists(motif_file):
            raise FileNotFoundError('The file containing all the homer motifs must be in '
                                    'the directory provided as input for homer parse.\n'
                                    'Please pass a directory that contains a file: homerMotifs.all.motifs')

        if not os.access(motif_file, os.R_OK):
            raise PermissionError('The file `homerMotifs.all.motifs` in the passed directory for '
                                  'homer output parsing is not readable.')

        locationFilePath = os.path.join(homer_output_dir, 'homer_locations.txt')

        if not os.path.exists(locationFilePath):
            raise FileNotFoundError('The file containing all the homer motifs must be in '
                                    'the directory provided as input for homer parse.\n'
                                    'Please pass a directory that contains a file: homer_locations.txt')

        if not os.access(locationFilePath, os.R_OK):
            raise PermissionError('The file `homer_locations.txt` in the passed directory for '
                                  'homer output parsing is not readable.')

        motifList, motifDict, pwmList = [], {}, []
        homerFile = open(motif_file, 'r')
        for line in homerFile:
            if '>' in line:
                if len(motifDict) != 0:
                    motifDict['pwm'] = pwmList
                    pwmList = []
                    motifDict['Locations'] = []
                    motifList.append(motifDict)
                    motifDict = {}
                elems = line.split()
                motif = elems[0].replace('>', '')
                motifDict['Iupac_signature'] = motif
                p_val = float(elems[5].split(',')[2].split(':')[1])
                motifDict['p-value'] = p_val
            else:
                elems = line.split()
                rowList = []
                rowList.append(('A', float(elems[0])))
                rowList.append(('C', float(elems[1])))
                rowList.append(('G', float(elems[2])))
                rowList.append(('T', float(elems[3])))
                pwmList.append(rowList)


        locationFile = open(locationFilePath, 'r')
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


        return motifList

    def parseGIBBSOutput(self, gibbs_output_dir):
        outputFileList, motifList = [], []
        for filename in os.listdir(gibbs_output_dir):
            outputFileList.append(os.path.join(gibbs_output_dir,filename))

        for outputFilePath in outputFileList:
            gibbsFile = open(outputFilePath, 'r')
            motifDict, pwmList = {}, []
            processPWM, processLoc, gotSig, motifIncluded = False, False, False, False

            # TODO: keeping p-value as -1 until I understand the output stats better
            motifDict['Locations'] = []
            for line in gibbsFile:
                if 'nMotifLen' in line:
                    MotifLen = int(line.split()[2])
                if processLoc is True:
                    if '****' in line:
                        processLoc = False
                        gotSig = False
                        motifDict['p-value'] = -1.0

                        a = []
                        c = []
                        g = []
                        t = []
                        for row in motifDict['pwm']:
                            a.append(row[0][1])
                            c.append(row[1][1])
                            g.append(row[2][1])
                            t.append(row[3][1])

                        motifStr = '>test\n'
                        motifStr += 'A ' + str(a).replace(',', '') + '\n'
                        motifStr += 'C ' + str(c).replace(',', '') + '\n'
                        motifStr += 'G ' + str(g).replace(',', '') + '\n'
                        motifStr += 'T ' + str(t).replace(',', '') + '\n'
                        handle = StringIO(motifStr)
                        BioMotif = motifs.read(handle, 'jaspar')
                        motifDict['Iupac_signature'] = str(BioMotif.degenerate_consensus)

                        for m in motifList:
                            if motifDict['Iupac_signature'] == m['Iupac_signature']:
                                motifIncluded = True
                        if not motifIncluded:
                            if len(motifDict['pwm']) != len(motifDict['Iupac_signature']):
                                print(outputFilePath)
                                print(motifDict['Iupac_signature'])
                                print(len(motifDict['pwm']))
                            motifList.append(motifDict)
                        motifDict = {}
                        motifDict['Locations'] = []
                        motifIncluded = False
                        pwmList = []
                    elif 'Num Motifs' not in line:
                        elems = line.split()
                        if not gotSig:
                            motif = elems[4]
                            gotSig = True
                        locList = []
                        if len(line.split()) == 10:
                            locList.append(elems[9])
                            locList.append(elems[2])
                            locList.append(elems[6])
                            if elems[8] == 'F':
                                locList.append('+')
                            else:
                                locList.append('-')
                        elif len(line.split()) == 9:
                            locList.append(elems[8])
                            locList.append(elems[2])
                            locList.append(elems[5])
                            if elems[7] == 'F':
                                locList.append('+')
                            else:
                                locList.append('-')
                        motifDict['Locations'].append(locList)
                elif processPWM is True:
                    if 'Background' in line:
                        processPWM = False
                        motifDict['pwm'] = pwmList
                    elif '|' in line:
                        before = after
                        after = int(line.split()[0])
                        if before != -1 and after != -1:
                            if (after - before) != 1:
                                for i in range(0, (before - after)):
                                    rowList = []
                                    rowList.append(('A', .25))
                                    rowList.append(('C', .25))
                                    rowList.append(('G', .25))
                                    rowList.append(('T', .25))
                                    pwmList.append(rowList)
                        elems = line.split()
                        rowList = []
                        rowList.append(('A', float(elems[2])))
                        rowList.append(('C', float(elems[4])))
                        rowList.append(('G', float(elems[5])))
                        rowList.append(('T', float(elems[3])))
                        pwmList.append(rowList)
                elif 'columns' in line:
                    motifLength = int(line.split()[0])
                    processLoc = True
                elif 'Motif probability model' in line:
                    processPWM = True
                    before = -1
                    after = -1
        return motifList
    """
