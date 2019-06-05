# -*- coding: utf-8 -*-
#BEGIN_HEADER
import os
import MotifUtils.Utils.MemeUtil as MU
import MotifUtils.Utils.GibbsUtil as GU
import MotifUtils.Utils.HomerUtil as HU
import MotifUtils.Utils.MotifSetUtil as MSU
import MotifUtils.Utils.Downloads as MD
from DataFileUtil.DataFileUtilClient import DataFileUtil
from copy import deepcopy

#END_HEADER


class MotifUtils:
    '''
    Module Name:
    MotifUtils

    Module Description:
    A KBase module: MotifUtils
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = ""
    GIT_COMMIT_HASH = ""

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.shared_folder = config['scratch']
        #END_CONSTRUCTOR
        pass


    def UploadFromGibbs(self, ctx, params):
        """
        :param params: instance of type "UploadMEMEInParams" -> structure:
           parameter "path" of String, parameter "ws_name" of String,
           parameter "obj_name" of String
        :returns: instance of type "UploadOutput" -> structure: parameter
           "obj_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN UploadFromGibbs
        print('Extracting motifs')
        motifList = GU.parse_gibbs_output(params['path'])
        print(motifList)

        MSO = {}
        MSO['Condition'] = 'Temp'
        MSO['SequenceSet_ref'] = '123'
        MSO['Motifs'] = []
        MSO['Alphabet'] = ['A','C','G','T']
        MSO['Background'] = MSU.GetBackground()
        for letter in MSO['Alphabet']:
            MSO['Background'][letter] = 0.0

        MSU.parseMotifList(motifList,MSO)
        MSU.CheckLength(MSO,params['min_len'],params['max_len'])
        for motif in MSO['Motifs']:
            for letter in MSO['Alphabet']:
                if len(motif['PWM'][letter]) != len(motif['Iupac_sequence']):
                    print('CAUGHT PWM ERROR HERE')
                    exit(1)
        if 'absolute_locations' in params:
            for motif in MSO['Motifs']:
                for loc in motif['Motif_Locations']:
                    if loc['sequence_id'] in params['absolute_locations']:
                        loc['sequence_id'] = params['contig']
                        absStart = int(params['start'])
                        loc['start'] = absStart
                        loc['end'] = absStart + loc['end']

        dfu = DataFileUtil(self.callback_url)
        save_objects_params = {}
        save_objects_params['id'] = dfu.ws_name_to_id(params['ws_name'])
        save_objects_params['objects'] = [{'type': 'KBaseGeneRegulation.MotifSet' , 'data' : MSO , 'name' : params['obj_name']}]

        info = dfu.save_objects(save_objects_params)[0]
        print('SAVED OBJECT')
        print(info)
        motif_set_ref = "%s/%s/%s" % (info[6], info[0], info[4])
        print(motif_set_ref)
        output = {'obj_ref' : motif_set_ref}
        print(output)
        #END UploadFromGibbs

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method UploadFromGibbs return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def UploadFromHomer(self, ctx, params):
        """
        :param params: instance of type "UploadHomerInParams" -> structure:
           parameter "path" of String, parameter "ws_name" of String,
           parameter "obj_name" of String, parameter "location_path" of String
        :returns: instance of type "UploadOutput" -> structure: parameter
           "obj_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN UploadFromHomer
        print('Extracting motifs')
        motifList = HU.parse_homer_output(params['path'],params['location_path'])
        print(motifList)

        MSO = {}
        MSO['Condition'] = 'Temp'
        MSO['SequenceSet_ref'] = '123'
        MSO['Motifs'] = []
        MSO['Alphabet'] = ['A','C','G','T']
        MSO['Background'] = {}
        for letter in MSO['Alphabet']:
            MSO['Background'][letter] = 0.0

        MSU.parseMotifList(motifList,MSO)
        MSU.CheckLength(MSO,params['min_len'],params['max_len'])
        if 'absolute_locations' in params:
            for motif in MSO['Motifs']:
                for loc in motif['Motif_Locations']:
                    if loc['sequence_id'] in params['absolute_locations']:
                        loc['sequence_id'] = params['contig']
                        absStart = int(params['start'])
                        loc['start'] = absStart
                        loc['end'] = absStart + loc['end']

        dfu = DataFileUtil(self.callback_url)
        save_objects_params = {}
        save_objects_params['id'] = dfu.ws_name_to_id(params['ws_name'])
        save_objects_params['objects'] = [{
            'type': 'KBaseGeneRegulation.MotifSet',
            'data': MSO,
            'name': params['obj_name']
        }]

        info = dfu.save_objects(save_objects_params)[0]
        print('SAVED OBJECT')
        print(info)
        motif_set_ref = "%s/%s/%s" % (info[6], info[0], info[4])
        print(motif_set_ref)
        output = {'obj_ref' : motif_set_ref}
        print(output)
        #END UploadFromHomer

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method UploadFromHomer return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def UploadFromMEME(self, ctx, params):
        """
        :param params: instance of type "UploadGibbsInParams" -> structure:
           parameter "path" of String, parameter "ws_name" of String,
           parameter "obj_name" of String
        :returns: instance of type "UploadOutput" -> structure: parameter
           "obj_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN UploadFromMEME
        print('Extracting motifs')
        motifList = MU.parse_meme_output(params['path'])
        print(motifList)


        MSO = {}
        MSO['Condition'] = 'Temp'
        MSO['SequenceSet_ref'] = '123'
        MSO['Motifs'] = []
        MSO['Alphabet'] = ['A','C','G','T']
        MSO['Background'] = {}
        for letter in MSO['Alphabet']:
            MSO['Background'][letter] = 0.0

        MSU.parseMotifList(motifList,MSO)
        MSU.CheckLength(MSO,params['min_len'],params['max_len'])
        if 'absolute_locations' in params:
            for motif in MSO['Motifs']:
                for loc in motif['Motif_Locations']:
                    if loc['sequence_id'] in params['absolute_locations']:
                        loc['sequence_id'] = params['contig']
                        absStart = int(params['start'])
                        loc['start'] = absStart
                        loc['end'] = absStart + loc['end']

        dfu = DataFileUtil(self.callback_url)
        save_objects_params = {}
        save_objects_params['id'] = dfu.ws_name_to_id(params['ws_name'])
        save_objects_params['objects'] = [{'type': 'KBaseGeneRegulation.MotifSet' , 'data' : MSO , 'name' : params['obj_name']}]

        info = dfu.save_objects(save_objects_params)[0]
        print('SAVED OBJECT')
        print(info)
        motif_set_ref = "%s/%s/%s" % (info[6], info[0], info[4])
        print(motif_set_ref)
        output = {'obj_ref' : motif_set_ref}
        print(output)

        #END UploadFromMEME

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method UploadFromMEME return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def UploadFromJASPAR(self, ctx, params):
        """
        :param params: instance of type "UploadJASPARInParams" -> structure:
           parameter "path" of String, parameter "ws_name" of String,
           parameter "obj_name" of String
        :returns: instance of type "UploadOutput" -> structure: parameter
           "obj_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN UploadFromJASPAR
        #END UploadFromJASPAR

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method UploadFromJASPAR return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def UploadFromTRANSFAC(self, ctx, params):
        """
        :param params: instance of type "UploadTRANSFACInParams" ->
           structure: parameter "path" of String, parameter "ws_name" of
           String, parameter "obj_name" of String
        :returns: instance of type "UploadOutput" -> structure: parameter
           "obj_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN UploadFromTRANSFAC
        #END UploadFromTRANSFAC

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method UploadFromTRANSFAC return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def DownloadMotifSet(self, ctx, params):
        """
        :param params: instance of type "DownloadParams" -> structure:
           parameter "ws_name" of String, parameter "source_ref" of String,
           parameter "format" of String
        :returns: instance of type "DownloadOutput" -> structure: parameter
           "destination_dir" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN DownloadMotifSet
        #fname = params[]
        dfu = DataFileUtil(self.callback_url)
        get_object_params = {'object_refs' : [params['source_ref']]} #grab motifset object
        MSO = dfu.get_objects(get_object_params)['data'][0]['data']
        output = ''
        if params['format'] == 'MEME':
            output = MD.MotifSetToMEME(MSO)
        else:
            print('FORMAT IS NOT RECOGNIZED OR SUPPORTED')
            print('Supported Formats: MEME JASPAR TRANSFAC')
            print('Implemented: MEME')
        outFilePath = '/kb/module/work/tmp/' + params['outname']
        with open(outFilePath) as outFile:
            outFile.write(output)
        output = {'destination_path': outFilePath}


        #TODO: add this...
        #END DownloadMotifSet

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method DownloadMotifSet return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def importFromNarrative(self, ctx, params):
        """
        :param params: instance of type "ImportNarrativeInParams" ->
           structure: parameter "ws_name" of String, parameter "path" of
           String, parameter "format" of String, parameter "obj_name" of
           String
        :returns: instance of type "ImportNarrativeOutParams" -> structure:
           parameter "obj_ref" of String
        """
        # ctx is the context object
        # return variables are: out
        #BEGIN importFromNarrative

        file_path = ''
        #Move Staging file to work
        if params.get('local_path'):
            file_path = params.get('local_path')
        elif params.get('shock_id'):
            file_path = self.dfu.shock_to_file(
                {'shock_id': params['shock_id'],
                 'file_path': self.scratch}).get('file_path')
        elif params.get('staging_path'):
            file_path = self.dfu.download_staging_file(
                        {'staging_file_subdir_path': params.get('staging_path')}
                        ).get('copy_file_path')

        format = params['format']
        new_params = dict(params)
        new_params.pop('format',None)
        new_params.pop('staging_path',None)
        new_params.pop('local_path',None)
        new_params.pop('shock_id',None)
        new_params['path'] = file_path

        validFormats = ['MEME','JASPAR','GIBBS','HOMER','TRANSFAC','GENERIC']

        out = {}

        if format == 'MEME':
            out = self.UploadFromMEME(ctx,new_params)[0]
            #print(out)
            #print('NOT YET IMPLENTED')
        if format == 'JASPAR':
            return self.UploadFromJASPAR(ctx,new_params)
            print('NOT YET IMPLENTED')
        if format == 'GIBBS':
            out = self.UploadFromGibbs(ctx,new_params)
            print('NOT YET IMPLENTED')
        if format == 'HOMER':
            print('NOT YET IMPLENTED')
        if format == 'TRANSFAC':
            return self.UploadFromTRANSFAC(ctx,new_params)
            print('NOT YET IMPLENTED')
        if format == 'GENERIC':
            print('NOT YET IMPLENTED')

        #END importFromNarrative

        # At some point might do deeper type checking...
        if not isinstance(out, dict):
            raise ValueError('Method importFromNarrative return value ' +
                             'out is not type dict as required.')
        # return the results
        return [out]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
