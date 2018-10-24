# -*- coding: utf-8 -*-
#BEGIN_HEADER
import MotifUtils.Utils.ParseMotifFile as PMF
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

        #Move Staging file to work
        validFormats = ['MEME','JASPAR','GIBBS','HOMER','TRANSFAC','GENERIC']

        if format == 'MEME':
            newparams['ws_name'] = params['ws_name']
            #newparams
            print('NOT YET IMPLENTED')
        if format == 'JASPAR':
            print('NOT YET IMPLENTED')
        if format == 'GIBBS':
            print('NOT YET IMPLENTED')
        if format == 'HOMER':
            print('NOT YET IMPLENTED')
        if format == 'TRANSFAC':
            print('NOT YET IMPLENTED')
        if format == 'GENERIC'
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
