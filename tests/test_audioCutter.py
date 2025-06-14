import unittest
from contextlib import redirect_stdout
import io

from functools import wraps

from unittest.mock import patch, MagicMock, mock_open

patch('loggingSettings.logger_wrapper', lambda x: x).start()
   
from audioCutter import AudioCutter


class test_audioCutter(unittest.TestCase):
    

    def setUp(self):
        with patch("builtins.open", mock_open(read_data="data")) as mock_file:
            self.test_audiocutter = AudioCutter('./tests/dummy.mp3', '.tests/dummy_outputs/')
         
    def tearDown(self):
        del self.test_audiocutter   
    
    def test_audiocutter_attributes(self):
        self.assertTrue(hasattr(self.test_audiocutter, 'source_path'))
        self.assertTrue(hasattr(self.test_audiocutter, 'output_path'))   
        
    def test_time_to_miliseconds(self):
        self.assertEqual(self.test_audiocutter.time_to_miliseconds("00:09:42"), 9056)
        with self.assertRaises(ValueError):
            self.test_audiocutter.time_to_miliseconds("MM:09:42") 
        
    def test_time_to_seconds(self):
        self.assertEqual(self.test_audiocutter.time_to_seconds("00:09:42"), 9.56)
        with self.assertRaises(ValueError):
            self.test_audiocutter.time_to_seconds("00:MM:42")