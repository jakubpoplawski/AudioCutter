import unittest

import paramiko

from paramiko import SSHClient
import subprocess, sys

from functools import wraps
import io

from unittest.mock import patch, MagicMock, Mock

# patch('loggingSettings.logger_wrapper', lambda x: x).start()
   
from audioSender import SFTPClient


class test_SFTPClient(unittest.TestCase):
    

    def setUp(self):
        patch('loggingSettings.logger_wrapper', lambda x: x).start()
        self.test_SFTPClient = SFTPClient('0000', 'blah', 'blahpass',
                                          ['000.000.0.101', '000.000.0.102'])


        
    def tearDown(self):
        del self.test_SFTPClient   
        
    def test_ip_scanner_attributes(self):
        self.assertTrue(hasattr(self.test_SFTPClient, 
                                'host_ip'))
        self.assertTrue(hasattr(self.test_SFTPClient, 
                                'port'))       
        self.assertTrue(hasattr(self.test_SFTPClient, 
                                'user'))
        self.assertTrue(hasattr(self.test_SFTPClient, 
                                'password'))
        self.assertTrue(hasattr(self.test_SFTPClient, 
                                'ip_list'))
        self.assertTrue(hasattr(self.test_SFTPClient, 
                                'SSH_Client'))
    

    def test_ssh_connect(self):
        self.test_SFTPClient.host_ip = '000.000.0.101'
        
        mock_SSHClient = self.test_SFTPClient.SSH_Client
        mock_SSHClient.connect = MagicMock()

        self.test_SFTPClient.ssh_connect()  
        mock_SSHClient.connect.assert_called_with(
            '000.000.0.101', username='blah', password='blahpass', 
            look_for_keys=True, port='0000', timeout=3)
        
    def test_ssh_scan_connect(self):
        mock_SSHClient = self.test_SFTPClient.SSH_Client
        mock_SSHClient.connect = MagicMock()

        self.test_SFTPClient.ssh_scan_connect()  
        mock_SSHClient.connect.assert_any_call(
            '000.000.0.101', username='blah', password='blahpass', 
            look_for_keys=True, port='0000', timeout=3)  
        # mock_SSHClient.connect.assert_any_call(
        #     '000.000.0.102', username='blah', password='blahpass', 
        #     look_for_keys=True, port='0000', timeout=3)  
        
        
        # Not called because it mocks a successful connection. 
        # How to mock second connection as succesful?