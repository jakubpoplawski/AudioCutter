import unittest
import subprocess, sys

from functools import wraps
import io

from unittest.mock import patch, MagicMock, Mock

patch('loggingSettings.logger_wrapper', lambda x: x).start()
   
from ipScanner import IPScanner


class test_ipScanner(unittest.TestCase):
    

    def setUp(self):
        self.test_ip_scanner = IPScanner('0000', 
                                    '000.000.0.0/24',
                                    '000\.\d{1,3}\.\d{1,3}\.\d{1,3}')
        
    def tearDown(self):
        del self.test_ip_scanner   
        
    def test_ip_scanner_attributes(self):
        self.assertTrue(hasattr(self.test_ip_scanner, 
                                'port'))
        self.assertTrue(hasattr(self.test_ip_scanner, 
                                'ip_range'))       
        self.assertTrue(hasattr(self.test_ip_scanner, 
                                'regex_ip_filter')) 
        
    def test_ip_scanner_scan_ips(self): 
        subprocess_mock = subprocess
        subprocess_mock.check_output = MagicMock()
        mock_stdout = MagicMock()
        mock_stdout.configure_mock(
            **{
               'stdout.decode.return_value': 
                   '000.000.0.101\n000.000.0.102\n' 
            }
        )
        subprocess_mock.run = MagicMock(return_value=mock_stdout)

        
        self.assertEqual(self.test_ip_scanner.scan_ips(), 
                         ['000.000.0.101', '000.000.0.102'])

        subprocess_mock.run.assert_called_with(
            "nmap -sT -p 0000 000.000.0.0/24 | grep -oP "\
                "'000\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}'", 
            stdout=-1, timeout=None, check=True, shell=True)      

