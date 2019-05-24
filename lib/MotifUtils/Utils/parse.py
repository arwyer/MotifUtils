import logging
import os
from urllib import request, parse

from installed_clients.DataFileUtilClient import DataFileUtil


class MotifParser:
    def __init__(self, callback, motifformat, scratch):
        self.scratch = scratch
        self.dfu = DataFileUtil(callback)
        self.motifformat = motifformat

        logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                            level=logging.INFO)

    def parseMotif(self, file):
        # remove empty keys from file
        removekeys = []
        for k, v in file.items():
            if v == '' or v == None or v == 'NA':
                removekeys.append(k)

        for k in removekeys:
            file.pop(k)

        if len(file) > 1 or len(file) < 1:
            raise ValueError('Please input a single file location within the parameters:\n' +
                                'file = {\n' +
                                '\t\'shock_id\': \'SHOCKID\',\n' +
                                '\t\'ftp_url\': \'FTPURL\',\n' +
                                '\t\'path\': \'CONTAINERFILEPATH\',\n' +
                                '}')

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
        elif 'path' if file:
            if not os.path.exists(file['path']):
                raise ValueError('The file specified from the input parameter file, does not exists')

