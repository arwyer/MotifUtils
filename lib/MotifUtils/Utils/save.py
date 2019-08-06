import uuid
import logging
from pprint import pprint as pp

from installed_clients.DataFileUtilClient import DataFileUtil


class MotifSaver:
    def __init__(self, callback, scratch):
        self.scratch = scratch
        self.dfu = DataFileUtil(callback)
        logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                            level=logging.INFO)

    def saveMotifSet(self, motifset, params):
        if isinstance(motifset, list):
            logging.info('Saving multiple motifset objects...')
            # TODO: accept lists of constructed motif set object
            # TODO: check if list is a save_objects list or list of motifsets process accordingly
            # TODO: accept list of object names
            obj = self.dfu.save_objects({
                'id': self.dfu.ws_name_to_id(params['ws_name']),
                'objects': [{
                    'type': 'KBaseGeneRegulation.MotifSet',
                    'data': motifset[0],
                    'name': str(uuid.uuid4())
                }]
            })[0]

            return str(obj[6]) + "/" + str(obj[0]) + "/" + str(obj[4])
        elif isinstance(motifset, dict):
            logging.info('Saving a single motifset object...')
            # TODO: accept object name
            obj = self.dfu.save_objects({
                'id': self.dfu.ws_name_to_id(params['ws_name']),
                'objects': [{
                    'type': 'KBaseGeneRegulation.MotifSet',
                    'data': motifset,
                    'name': str(uuid.uuid4())
                }]
            })[0]

            return str(obj[6]) + "/" + str(obj[0]) + "/" + str(obj[4])
        else:
            raise ValueError('Input to motif saver should be either: ' + '\n'
                             '1. a list of constructed KBaseGeneRegulation.MotifSet objects (dictionary)\n' +
                             '2. a single KBaseGeneRegulation.MotifSet object (dictionary)')
