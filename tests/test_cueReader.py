import unittest
from contextlib import redirect_stdout
import io

from functools import wraps

from unittest.mock import patch, MagicMock, mock_open

patch('loggingSettings.logger_wrapper', lambda x: x).start()
   
from cueReader import CueSheet, CueTrack


class test_CueSheet(unittest.TestCase):
    
    # def mock_decorator(*args, **kwargs):
    #     """Decorate by doing nothing."""
    #     def decorator(f):
    #         @wraps(f)
    #         def decorated_function(*args, **kwargs):
    #             return f(*args, **kwargs)
    #         return decorated_function
    #     return decorator

    #@classmethod
    def setUp(self):
        #patch('loggingSettings.logger_wrapper', test_CueSheet.mock_decorator).start()
        
        self.test_cuesheet = CueSheet('./tests/dummy_cue.cue')
         
    #@classmethod
    def tearDown(self):
        del self.test_cuesheet   
    
    def test_cuesheet_attributes(self):
        self.assertTrue(hasattr(self.test_cuesheet, 'performer'))
        self.assertTrue(hasattr(self.test_cuesheet, 'title'))    
        self.assertTrue(hasattr(self.test_cuesheet, 'album_file_name'))    
        self.assertTrue(hasattr(self.test_cuesheet, 'tracks'))    
        self.assertTrue(hasattr(self.test_cuesheet, 'execution_plan'))  
    
    # @patch('info')
    def test_eval_line(self):
        dummy_performer_line = 'PERFORMER "John Doe"\n'
        tested_performer_line = self.test_cuesheet.execution_plan['performer']
        self.assertEqual(self.test_cuesheet.eval_line(tested_performer_line, 
                                                      dummy_performer_line), 
                                                    "John Doe")

        dummy_album_title_line = 'TITLE "Book"\n'
        album_title_regex = self.test_cuesheet.execution_plan['title']
        self.assertEqual(self.test_cuesheet.eval_line(
            album_title_regex, dummy_album_title_line), "Book")  
          
        dummy_album_file_name_line = 'FILE "book.mp3" MP3\n'
        album_file_name_regex = self.test_cuesheet.execution_plan['file']
        self.assertEqual(self.test_cuesheet.eval_line(
            album_file_name_regex, dummy_album_file_name_line), "book.mp3")
        
        dummy_track_beggining_line = '\tTRACK 00 AUDIO\n'
        album_track_beggining_regex = self.test_cuesheet.\
                                        execution_plan['track_beginning']
        self.assertEqual(self.test_cuesheet.eval_line(
            album_track_beggining_regex, 
            dummy_track_beggining_line)[0], 
            "00") 
        self.assertIsInstance(self.test_cuesheet.eval_line(
            album_track_beggining_regex, 
            dummy_track_beggining_line)[1], 
            CueTrack)
    
    