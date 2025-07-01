import unittest

import paramiko

from paramiko import SSHClient
import subprocess, sys

from functools import wraps
import io

from unittest.mock import patch, MagicMock, Mock, mock_open

patch('loggingSettings.logger_wrapper', lambda x: x).start()

from cueReader import CueSheet
from audioCutter import AudioCutter
from audioSender import SFTPClient



class test_SFTPClient(unittest.TestCase):
    

    def setUp(self):
        self.test_SFTPClient = SFTPClient('0000', 'blah', 'blahpass',
                                          ['000.000.0.101', 
                                           '000.000.0.102'])
        
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
        
    def test_ssh_scan_connect_good(self):
        mock_SSHClient = self.test_SFTPClient.SSH_Client
   
               
        mock_SSHClient.connect = MagicMock(return_value=True, 
                                           side_effect=[TimeoutError, 
                                                        True])
        
        self.test_SFTPClient.ssh_scan_connect()  
        mock_SSHClient.connect.assert_any_call(
            '000.000.0.101', username='blah', password='blahpass', 
            look_for_keys=True, port='0000', timeout=3)
        mock_SSHClient.connect.assert_any_call(
            '000.000.0.102', username='blah', password='blahpass', 
            look_for_keys=True, port='0000', timeout=3) 
        
    def test_ssh_scan_connect_bad(self):
        mock_SSHClient = self.test_SFTPClient.SSH_Client
   
               
        mock_SSHClient.connect = MagicMock(return_value=True, 
                                           side_effect=[TimeoutError, 
                                                        TimeoutError])

        with self.assertRaises(TimeoutError):
            self.test_SFTPClient.ssh_scan_connect()  
         
        mock_SSHClient.connect.assert_any_call(
            '000.000.0.101', username='blah', password='blahpass', 
            look_for_keys=True, port='0000', timeout=3)
        mock_SSHClient.connect.assert_any_call(
            '000.000.0.102', username='blah', password='blahpass', 
            look_for_keys=True, port='0000', timeout=3)  
    
    def test_ssh_disconnect(self):
        mock_SSHClient = self.test_SFTPClient.SSH_Client
   
               
        mock_SSHClient.connect = MagicMock(return_value=True, 
                                           side_effect=[TimeoutError, 
                                                        True])
               
        mock_SSHClient.close = MagicMock()


        self.test_SFTPClient.ssh_scan_connect()  
        self.test_SFTPClient.ssh_disconnect()      
         
        mock_SSHClient.close.assert_any_call()

    def test_ssh_create_directory_exists(self):
        mock_SSHClient = self.test_SFTPClient.SSH_Client
   
        mock_sftp_client = MagicMock()
        mock_sftp_client.stat.return_value = True
        mock_SSHClient.open_sftp = MagicMock(
            return_value=mock_sftp_client)
        mock_SSHClient.mkdir = MagicMock()  
        
        self.test_SFTPClient.ssh_create_directory('Audiobooks/the_book')  
              
        mock_sftp_client.stat.assert_called() 
        mock_sftp_client.mkdir.assert_not_called() 
                      
    def test_ssh_create_directory_not_exists(self):
        mock_SSHClient = self.test_SFTPClient.SSH_Client
   
        mock_sftp_client = MagicMock()
        mock_sftp_client.stat.side_effect = IOError
        mock_SSHClient.open_sftp = MagicMock(
            return_value=mock_sftp_client)
        mock_sftp_client.mkdir = MagicMock()

        self.test_SFTPClient.ssh_create_directory('Audiobooks/the_book')  
              
        mock_sftp_client.stat.assert_called() 
        mock_sftp_client.mkdir.assert_called() 

    def test_ssh_upload_file_exits_on_target(self):
        mock_SSHClient = self.test_SFTPClient.SSH_Client
   
        mock_sftp_client = MagicMock()
        mock_sftp_client.stat.return_value = True
        mock_SSHClient.open_sftp = MagicMock(
            return_value=mock_sftp_client)
        mock_sftp_client.put = MagicMock()

        self.test_SFTPClient.ssh_upload_file(
            'Documents/the_book/track_01.mp3', 
            'Audiobooks/the_book/track_01.mp3')  
              
        mock_sftp_client.stat.assert_called() 
        mock_sftp_client.put.assert_not_called()        

    def test_ssh_upload_file_not_exits_on_local(self):
        mock_SSHClient = self.test_SFTPClient.SSH_Client
   
        mock_sftp_client = MagicMock()
        mock_sftp_client.stat.side_effect = FileNotFoundError
        mock_SSHClient.open_sftp = MagicMock(
            return_value=mock_sftp_client)
        mock_sftp_client.put = MagicMock()
        mock_sftp_client.put.side_effect = FileNotFoundError

        with self.assertRaises(FileNotFoundError):
            self.test_SFTPClient.ssh_upload_file(
                'Documents/the_book/track_01.mp3', 
                'Audiobooks/the_book/track_01.mp3')  
              
        mock_sftp_client.stat.assert_called() 
        mock_sftp_client.put.assert_called()        

class test_SFTPClient_ssh_upload_album(unittest.TestCase):


    def setUp(self):
        with patch("builtins.open", 
                   mock_open(read_data="data")) as mock_file:
            self.test_audiocutter = AudioCutter('tests/dummy.mp3', 
                                                'tests/dummy_outputs/')
        
        self.test_cuesheet = CueSheet('tests/dummy_cue.cue')
        self.test_cuesheet.sheet_reader_liner()
        self.test_cuesheet.add_ending_time()
        self.test_SFTPClient = SFTPClient('0000', 'blah', 'blahpass',
                                          ['000.000.0.101', 
                                           '000.000.0.102'])
        
    def tearDown(self):
        del self.test_audiocutter   
        del self.test_cuesheet
        del self.test_SFTPClient
        
    def test_ssh_upload_album(self):
        mock_SSHClient = self.test_SFTPClient.SSH_Client
   
        mock_sftp_client = MagicMock()
        mock_SSHClient.open_sftp = MagicMock(
            return_value=mock_sftp_client)
        self.test_SFTPClient.ssh_create_directory = MagicMock()
        self.test_SFTPClient.ssh_upload_file = MagicMock()       
        
        
        test_track_list = list(self.test_cuesheet.tracks.values())
        self.test_SFTPClient.ssh_upload_album(test_track_list, 
                                            'Documents/',
                                            'Audiobooks/',
                                            'the_book') 
        
        self.assertEqual(len(test_track_list), 3)
        
        self.test_SFTPClient.ssh_create_directory.assert_called_with(
            'Audiobooks/the_book/')

        self.test_SFTPClient.ssh_upload_file.assert_any_call(
            'Documents/0000 - book.mp3', 
            'Audiobooks/the_book/0000 - book.mp3')
        self.test_SFTPClient.ssh_upload_file.assert_any_call(
            'Documents/0001 - book.mp3', 
            'Audiobooks/the_book/0001 - book.mp3')
        self.test_SFTPClient.ssh_upload_file.assert_any_call(
            'Documents/0002 - book.mp3', 
            'Audiobooks/the_book/0002 - book.mp3')