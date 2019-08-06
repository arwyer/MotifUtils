# -*- coding: utf-8 -*-
#BEGIN_HEADER
import logging
import os

from .Utils.parse import MotifParser
from .Utils.save import MotifSaver
from .Utils.GibbsUtil import GibbsUtil as Gibbs
from .Utils.HomerUtil import HomerUtils as Homer
from .Utils.MemeUtil import MEMEUtil as MEME
from .Utils.MFMDUtil import MFMDUtil as MFMD

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
    GIT_COMMIT_HASH = "3a4cf6a38e20f93bda86196af49242b0f7c7385b"

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

        self.MotifParser = MotifParser(config)
        self.MotifSaver = MotifSaver(self.callback_url, self.shared_folder)

        #END_CONSTRUCTOR
        pass


    def uploadMotifSet(self, ctx, params):
        """
        :param params: instance of type "uploadParams" -> structure:
           parameter "format" of type "motif_format" (Input/Output motif
           format @range("MEME", "JASPAR", "GIBBS", "HOMER", "TRANSFAC",
           "MFMD")), parameter "path" of String, parameter "obj_name" of
           String, parameter "ws_name" of type "workspace_name" (workspace
           name of the object)
        :returns: instance of type "UIOutParams" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String,
           parameter "motif_obj" of type "MotifSetRef" (Ref to a sequence set
           @id ws KBaseGeneRegulation.MotifSet)
        """
        # ctx is the context object
        # return variables are: out
        #BEGIN uploadMotifSet

        # params['format'] is the motif upload format

        motifset = MotifParser.parseMotif(params)
        out = MotifSaver.saveMotifSet(motifset)

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
           @range("MEME", "JASPAR", "GIBBS", "HOMER", "TRANSFAC", "MFMD")),
           parameter "file" of type "File" -> structure: parameter "path" of
           String, parameter "shock_id" of String, parameter "ftp_url" of
           String, parameter "ws_name" of type "workspace_name" (workspace
           name of the object), parameter "seq_set_ref" of type
           "SequenceSetRef" (Ref to a sequence set @id ws
           KBaseGeneRegulation.SequenceSet)
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

        out = self.MotifParser.parseMotif(params)
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
           @range("MEME", "JASPAR", "GIBBS", "HOMER", "TRANSFAC", "MFMD")),
           parameter "file" of type "File" -> structure: parameter "path" of
           String, parameter "shock_id" of String, parameter "ftp_url" of
           String, parameter "obj_name" of String, parameter "ws_name" of
           type "workspace_name" (workspace name of the object), parameter
           "seq_set_ref" of type "SequenceSetRef" (Ref to a sequence set @id
           ws KBaseGeneRegulation.SequenceSet)
        :returns: instance of type "MotifSetRef" (Ref to a sequence set @id
           ws KBaseGeneRegulation.MotifSet)
        """
        # ctx is the context object
        # return variables are: out
        #BEGIN saveMotifSet

        motifset = self.parseMotifSet(ctx, params)
        exit(motifset)

        out = self.MotifSaver.saveMotifSet(motifset, params)

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
           format @range("MEME", "JASPAR", "GIBBS", "HOMER", "TRANSFAC",
           "MFMD")), parameter "motifset" of type "MotifSetRef" (Ref to a
           sequence set @id ws KBaseGeneRegulation.MotifSet), parameter
           "ws_name" of type "workspace_name" (workspace name of the object)
        :returns: instance of type "UIOutParams" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String,
           parameter "motif_obj" of type "MotifSetRef" (Ref to a sequence set
           @id ws KBaseGeneRegulation.MotifSet)
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

    def UploadFromGibbs(self, ctx, params):
        """
        :param params: instance of type "UploadMEMEInParams" (Backwards
           compatability) -> structure: parameter "path" of String, parameter
           "ws_name" of String, parameter "obj_name" of String, parameter
           "absolute_locations" of mapping from String to String
        :returns: instance of type "UIOutParams" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String,
           parameter "motif_obj" of type "MotifSetRef" (Ref to a sequence set
           @id ws KBaseGeneRegulation.MotifSet)
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN UploadFromGibbs

        logging.error(
            'This old call to MotifUtils is deprecated. It does not account for a sequence object and therefore is\n'
            'unable to provide motif sequence information and has been deprecated.\n'
            'Please use parseMotifSet with the parameters:\n'
            'format = MEME or Homer or Gibbs or other\n'
            'ws_name = workspace name\n'
            'file = dictionary of \'shock_id\' \'ftp_url\' or \'path\'\n'
            'genome_ref = kbase reference to genome reference\n'
            'Please the spec file for more details.')

        raise ValueError('Deprecated method function UploadFromGibbs, use parseMotifSet or saveMotifSet')

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
        :returns: instance of type "UIOutParams" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String,
           parameter "motif_obj" of type "MotifSetRef" (Ref to a sequence set
           @id ws KBaseGeneRegulation.MotifSet)
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN UploadFromHomer

        logging.error(
            'This old call to MotifUtils is deprecated. It does not account for a sequence object and therefore is\n'
            'unable to provide motif sequence information and has been deprecated.\n'
            'Please use parseMotifSet with the parameters:\n'
            'format = MEME or Homer or Gibbs or other\n'
            'ws_name = workspace name\n'
            'file = dictionary of \'shock_id\' \'ftp_url\' or \'path\'\n'
            'genome_ref = kbase reference to genome reference\n'
            'Please the spec file for more details.')

        raise ValueError('Deprecated method function UploadFromHomer, use parseMotifSet or saveMotifSet')

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
        :returns: instance of type "UIOutParams" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String,
           parameter "motif_obj" of type "MotifSetRef" (Ref to a sequence set
           @id ws KBaseGeneRegulation.MotifSet)
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN UploadFromMEME
        logging.error(
            'This old call to MotifUtils is deprecated. It does not account for a sequence object and therefore is\n'
            'unable to provide motif sequence information and has been deprecated.\n'
            'Please use parseMotifSet with the parameters:\n'
            'format = MEME or Homer or Gibbs or other\n'
            'ws_name = workspace name\n'
            'file = dictionary of \'shock_id\' \'ftp_url\' or \'path\'\n'
            'genome_ref = kbase reference to genome reference\n'
            'Please the spec file for more details.')

        raise ValueError('Deprecated method function UploadFromMEME, use parseMotifSet or saveMotifSet')

        #END UploadFromMEME

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method UploadFromMEME return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
