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
        pp(motifset)
        exit()
        logging.info('Saving a single motifset object...')
        # TODO: accept object name
        obj = self.dfu.save_objects({
            'id': self.dfu.ws_name_to_id(params['ws_name']),
            'objects': [{
                'type': 'KBaseGeneRegulation.MotifSet',
                'data': [motifset],
                'name': str(uuid.uuid4())
            }]
        })[0]

        return str(obj[6]) + "/" + str(obj[0]) + "/" + str(obj[4])
