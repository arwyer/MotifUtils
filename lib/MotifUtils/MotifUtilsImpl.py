# -*- coding: utf-8 -*-
#BEGIN_HEADER
import logging
import os

from installed_clients.KBaseReportClient import KBaseReport
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
    GIT_URL = "https://github.com/kbasecollaborations/MotifUtils.git"
    GIT_COMMIT_HASH = "731605fcff3dda908ed7f427205c5b304e4f4214"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.shared_folder = config['scratch']
        logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                            level=logging.INFO)
        #END_CONSTRUCTOR
        pass


    def uploadMotifSet(self, ctx, params):
        """
        :param params: instance of type "uploadParams" -> structure:
           parameter "format" of type "motif_format" (Input/Output motif
           format @range("MEME", "JASPAR", "GIBBS", "HOMER", "TRANSFAC")),
           parameter "path" of String, parameter "obj_name" of String,
           parameter "ws_name" of String
        :returns: instance of type "UIOutParams" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: out
        #BEGIN uploadMotifSet
        #END uploadMotifSet

        # At some point might do deeper type checking...
        if not isinstance(out, dict):
            raise ValueError('Method uploadMotifSet return value ' +
                             'out is not type dict as required.')
        # return the results
        return [out]

    def parseMotifSet(self, ctx, params):
        """
        :param params: instance of type "parseParams" -> structure: parameter
           "format" of type "motif_format" (Input/Output motif format
           @range("MEME", "JASPAR", "GIBBS", "HOMER", "TRANSFAC")), parameter
           "file" of type "File" -> structure: parameter "path" of String,
           parameter "shock_id" of String, parameter "ftp_url" of String
        :returns: instance of type "MotifSet" (Condition - description of
           conditionused to select sequences SequenceSet_ref - reference to
           sequenceset used to find motifs Motifs - list of motifs Alphabet -
           list of letters used in sequences, e.g. ['A','C','G','T'] for DNA
           Background - background frequencies of letters in alphabet) ->
           structure: parameter "Condition" of String, parameter
           "SequenceSet_ref" of String, parameter "Motifs" of list of type
           "Motif" (one of PWM or PFM must be included PWM - position weight
           matrix of motif PFM - position frequency matrix of motif
           Iupac_signature - motif represented in Iupac notation
           Motif_Locations - list of locations where motif has been found) ->
           structure: parameter "PWM" of mapping from String to list of
           Double, parameter "PFM" of mapping from String to list of Double,
           parameter "Iupac_sequence" of String, parameter "Motif_Locations"
           of list of type "Motif_Location" (sequence_id - id of sequence
           motif was found in associated sequenceset start - start of motif
           in the sequence end - end of motif in the sequence orientation -
           +/- sequence - actual motif sequence, might not match exactly to
           IUPAC) -> structure: parameter "sequence_id" of String, parameter
           "start" of Long, parameter "end" of Long, parameter "orientation"
           of String, parameter "sequence" of String, parameter "Alphabet" of
           list of String, parameter "Background" of mapping from String to
           Double
        """
        # ctx is the context object
        # return variables are: out
        #BEGIN parseMotifSet
        #END parseMotifSet

        # At some point might do deeper type checking...
        if not isinstance(out, dict):
            raise ValueError('Method parseMotifSet return value ' +
                             'out is not type dict as required.')
        # return the results
        return [out]

    def saveMotifSet(self, ctx, params):
        """
        :param params: instance of type "saveParams" -> structure: parameter
           "format" of type "motif_format" (Input/Output motif format
           @range("MEME", "JASPAR", "GIBBS", "HOMER", "TRANSFAC")), parameter
           "file" of type "File" -> structure: parameter "path" of String,
           parameter "shock_id" of String, parameter "ftp_url" of String,
           parameter "obj_name" of String
        :returns: instance of type "MotifSetRef" (Ref to a sequence set @id
           ws KBaseGeneRegulation.MotifSet)
        """
        # ctx is the context object
        # return variables are: out
        #BEGIN saveMotifSet
        #END saveMotifSet

        # At some point might do deeper type checking...
        if not isinstance(out, str):
            raise ValueError('Method saveMotifSet return value ' +
                             'out is not type str as required.')
        # return the results
        return [out]

    def downloadMotifSet(self, ctx, params):
        """
        :param params: instance of type "downloadParams" -> structure:
           parameter "format" of type "motif_format" (Input/Output motif
           format @range("MEME", "JASPAR", "GIBBS", "HOMER", "TRANSFAC")),
           parameter "motifset" of type "MotifSetRef" (Ref to a sequence set
           @id ws KBaseGeneRegulation.MotifSet), parameter "ws_name" of String
        :returns: instance of type "UIOutParams" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: out
        #BEGIN downloadMotifSet
        #END downloadMotifSet

        # At some point might do deeper type checking...
        if not isinstance(out, dict):
            raise ValueError('Method downloadMotifSet return value ' +
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
