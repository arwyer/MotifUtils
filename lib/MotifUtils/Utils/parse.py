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

    def get_background(self, seqfile):
        count = 0
        sfile = open(seqfile)
        FreqDict = {'A': 0, 'G': 0, 'C': 0, 'T': 0}
        for line in sfile:
            print(line)
            if count % 2 == 1:
                FreqDict['A'] += line.count('A')
                FreqDict['C'] += line.count('C')
                FreqDict['G'] += line.count('G')
                FreqDict['T'] += line.count('T')
            count += 1
        total = FreqDict['A'] + FreqDict['C'] + FreqDict['G'] + FreqDict['T']
        Background = {}

        Background['A'] = float(FreqDict['A']) / total
        Background['C'] = float(FreqDict['C']) / total
        Background['G'] = float(FreqDict['G']) / total
        Background['T'] = float(FreqDict['T']) / total
        return Background

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

    def parseMotif(self, params):
        # remove empty keys from file
        removekeys = []
        file = params['file']
        motifformat = params['format']
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

        MSO = {}

        alphabet = ['A', 'C', 'G', 'T']

        MSO['Condition'] = 'Temp'
        MSO['SequenceSet_ref'] = '123'
        MSO['Motifs'] = []
        MSO['Alphabet'] = alphabet
        MSO['Background'] = self.GetBackground(alphabet, file)

        MSO = motifinfo.parse(file)

        return MSO
