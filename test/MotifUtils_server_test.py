# -*- coding: utf-8 -*-
import unittest
import os
import time
import uuid

from pprint import pprint as pp
from os import environ
from configparser import ConfigParser

from biokbase.workspace.client import Workspace as workspaceService
from MotifUtils.MotifUtilsImpl import MotifUtils
from MotifUtils.MotifUtilsServer import MethodContext
from MotifUtils.authclient import KBaseAuth as _KBaseAuth
from installed_clients.DataFileUtilClient import DataFileUtil

from MotifUtils.Utils.save import MotifSaver

class MotifUtilsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = environ.get('KB_AUTH_TOKEN', None)
        config_file = environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('MotifUtils'):
            cls.cfg[nameval[0]] = nameval[1]
        # Getting username from Auth profile for token
        authServiceUrl = cls.cfg['auth-service-url']
        auth_client = _KBaseAuth(authServiceUrl)
        user_id = auth_client.get_user(token)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'MotifUtils',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = workspaceService(cls.wsURL)
        cls.serviceImpl = MotifUtils(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.callback_url = os.environ['SDK_CALLBACK_URL']
        cls.dfu = DataFileUtil(cls.callback_url)
        cls.MotifSaver = MotifSaver(cls.callback_url, cls.scratch )

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    def getWsClient(self):
        return self.__class__.wsClient

    def getWsName(self):
        if hasattr(self.__class__, 'wsName'):
            return self.__class__.wsName
        suffix = int(time.time() * 1000)
        wsName = "test_MotifUtils_" + str(suffix)
        ret = self.getWsClient().create_workspace({'workspace': wsName})  # noqa
        self.__class__.wsName = wsName
        return wsName

    def getImpl(self):
        return self.__class__.serviceImpl

    def getContext(self):
        return self.__class__.ctx

    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa

    def test_parse_meme(self):
        # Prepare test objects in workspace if needed using
        # self.getWsClient().save_objects({'workspace': self.getWsName(),
        #                                  'objects': []})
        #
        # Run your method by
        # ret = self.getImpl().your_method(self.getContext(), parameters...)
        #
        # Check returned data with
        # self.assertEqual(ret[...], ...) or other unittest methods
        file = {'path': '/kb/module/test/sample_data/meme/meme.txt'}
        params = {
            'format': 'MEME',
            'ws_name': 'rmr:narrative_1558461244202',
            'file': file,
            'genome_ref': '28598/18/1'
        }

        result = self.getImpl().parseMotifSet(self.getContext(), params)

        # validate dfu type spec
        resultobj = {
                'type': 'KBaseGeneRegulation.MotifSet',
                'data': result[0],
                'name': str(uuid.uuid4())
        }

        obj = self.getWsClient().save_objects({'workspace': self.getWsName(), 'objects': [resultobj]})[0]
        self.assertIn('KBaseGeneRegulation.MotifSet', obj[2])

    def test_parse_homer(self):
        # Prepare test objects in workspace if needed using
        # self.getWsClient().save_objects({'workspace': self.getWsName(),
        #                                  'objects': []})
        #
        # Run your method by
        # ret = self.getImpl().your_method(self.getContext(), parameters...)
        #
        # Check returned data with
        # self.assertEqual(ret[...], ...) or other unittest methods
        file = {'path': '/kb/module/test/sample_data/homer'}
        params = {
            'format': 'HOMER',
            'ws_name': 'rmr:narrative_1558461244202',
            'file': file,
            'genome_ref': '28598/18/1'
        }

        result = self.getImpl().parseMotifSet(self.getContext(), params)

        # validate dfu type spec
        resultobj = {
            'type': 'KBaseGeneRegulation.MotifSet',
            'data': result[0],
            'name': str(uuid.uuid4())
        }

        obj = self.getWsClient().save_objects({'workspace': self.getWsName(), 'objects': [resultobj]})[0]
        self.assertIn('KBaseGeneRegulation.MotifSet', obj[2])

    def test_parse_gibbs(self):
        # Prepare test objects in workspace if needed using
        # self.getWsClient().save_objects({'workspace': self.getWsName(),
        #                                  'objects': []})
        #
        # Run your method by
        # ret = self.getImpl().your_method(self.getContext(), parameters...)
        #
        # Check returned data with
        # self.assertEqual(ret[...], ...) or other unittest methods
        file = {'path': '/kb/module/test/sample_data/gibbs'}
        params = {
            'format': 'GIBBS',
            'ws_name': 'rmr:narrative_1558461244202',
            'file': file,
            'genome_ref': '28598/18/1'
        }

        result = self.getImpl().parseMotifSet(self.getContext(), params)

        # validate dfu type spec
        resultobj = {
            'type': 'KBaseGeneRegulation.MotifSet',
            'data': result[0],
            'name': str(uuid.uuid4())
        }

        obj = self.getWsClient().save_objects({'workspace': self.getWsName(), 'objects': [resultobj]})[0]
        self.assertIn('KBaseGeneRegulation.MotifSet', obj[2])

    def test_parse_gibbs(self):
        # Prepare test objects in workspace if needed using
        # self.getWsClient().save_objects({'workspace': self.getWsName(),
        #                                  'objects': []})
        #
        # Run your method by
        # ret = self.getImpl().your_method(self.getContext(), parameters...)
        #
        # Check returned data with
        # self.assertEqual(ret[...], ...) or other unittest methods
        file = {'path': '/kb/module/test/sample_data/gibbs'}
        params = {
            'format': 'GIBBS',
            'ws_name': 'rmr:narrative_1558461244202',
            'file': file,
            'genome_ref': '28598/18/1'
        }

        result = self.getImpl().parseMotifSet(self.getContext(), params)

        # validate dfu type spec
        resultobj = {
            'type': 'KBaseGeneRegulation.MotifSet',
            'data': result[0],
            'name': str(uuid.uuid4())
        }

        obj = self.getWsClient().save_objects({'workspace': self.getWsName(), 'objects': [resultobj]})[0]
        self.assertIn('KBaseGeneRegulation.MotifSet', obj[2])
    

    def test_parse_mfmd(self):
        # Prepare test objects in workspace if needed using
        # self.getWsClient().save_objects({'workspace': self.getWsName(),
        #                                  'objects': []})
        #
        # Run your method by
        # ret = self.getImpl().your_method(self.getContext(), parameters...)
        #
        # Check returned data with
        # self.assertEqual(ret[...], ...) or other unittest methods
        file = {'path': '/kb/module/test/sample_data/mfmd'}
        params = {
            'format': 'MFMD',
            'ws_name': 'rmr:narrative_1558461244202',
            'file': file,
            'genome_ref': '28598/18/1'
        }

        result = self.getImpl().parseMotifSet(self.getContext(), params)

        # validate dfu type spec
        resultobj = {
            'type': 'KBaseGeneRegulation.MotifSet',
            'data': result[0],
            'name': str(uuid.uuid4())
        }

        obj = self.getWsClient().save_objects({'workspace': self.getWsName(), 'objects': [resultobj]})[0]
        self.assertIn('KBaseGeneRegulation.MotifSet', obj[2])

    def test_parse_old_meme(self):
        file = {'path': '/kb/module/test/sample_data/mfmd'}
        params = {
            'path': '/kb/module/test/sample_data/meme/meme.txt',
            'ws_name': self.getWsName(),
            'obj_name': 'test_obj',
            'absolute_locations': ('test', 'test')
        }

        with self.assertRaises(ValueError):
            result = self.getImpl().UploadFromMEME(self.getContext(), params)

    def test_parse_old_homer(self):
        params = {
            'path': '/kb/module/test/sample_data/homer',
            'ws_name': self.getWsName(),
            'obj_name': 'test_obj',
            'absolute_locations': ('test', 'test')
        }

        with self.assertRaises(ValueError):
            result = self.getImpl().UploadFromHomer(self.getContext(), params)

    def test_parse_old_gibbs(self):
        params = {
            'path': '/kb/module/test/sample_data/gibbs',
            'ws_name': self.getWsName(),
            'obj_name': 'test_obj',
            'absolute_locations': ('test', 'test')
        }

        with self.assertRaises(ValueError):
            result = self.getImpl().UploadFromGibbs(self.getContext(), params)
