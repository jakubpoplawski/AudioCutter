import unittest
from contextlib import redirect_stdout
import io

from functools import wraps

from unittest.mock import patch, MagicMock, mock_open

patch('loggingSettings.logger_wrapper', lambda x: x).start()
   
from cueReader import CueSheet, CueTrack


class test_CueSheet(unittest.TestCase):
    

    def setUp(self):
        self.test_cuesheet = CueSheet('./tests/dummy_cue.cue')
         
    def tearDown(self):
        del self.test_cuesheet   
    
    def test_cuesheet_attributes(self):
        self.assertTrue(hasattr(self.test_cuesheet, 'performer'))
        self.assertTrue(hasattr(self.test_cuesheet, 'title'))    
        self.assertTrue(hasattr(self.test_cuesheet, 'album_file_name'))    
        self.assertTrue(hasattr(self.test_cuesheet, 'tracks'))    
        self.assertTrue(hasattr(self.test_cuesheet, 'execution_plan'))  
    
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
        album_file_name_regex = \
            self.test_cuesheet.execution_plan['file']
        self.assertEqual(self.test_cuesheet.eval_line(
            album_file_name_regex, dummy_album_file_name_line), 
                         "book.mp3")
        
        dummy_track_beggining_line = '\tTRACK 00 AUDIO\n'
        album_track_beggining_regex = \
            self.test_cuesheet.execution_plan['track_beginning']
        self.assertEqual(self.test_cuesheet.eval_line(
            album_track_beggining_regex, 
            dummy_track_beggining_line)[0], 
            "00") 
        self.assertIsInstance(self.test_cuesheet.eval_line(
            album_track_beggining_regex, 
            dummy_track_beggining_line)[1], 
            CueTrack)


    def test_sheet_reader_liner(self): 
        self.test_cuesheet.sheet_reader_liner()
        self.assertEqual(self.test_cuesheet.performer, "John Doe")
        self.assertEqual(self.test_cuesheet.title, "Book")
        self.assertEqual(self.test_cuesheet.album_file_name, "book.mp3")
  
        self.assertEqual(self.test_cuesheet.tracks['00'].\
            track_number, 1)   
        self.assertEqual(self.test_cuesheet.tracks['00'].\
            track_enumeration, 'TRACK 00') 
        self.assertEqual(self.test_cuesheet.tracks['00'].\
            track_performer, 'Jane Doe')  
        self.assertEqual(self.test_cuesheet.tracks['00'].\
            track_file_name, '0000 - book.mp3')   
        self.assertEqual(self.test_cuesheet.tracks['00'].\
            track_title, 'Start') 
        self.assertEqual(self.test_cuesheet.tracks['00'].\
            track_start_index, '00:00:00') 
        self.assertEqual(self.test_cuesheet.tracks['00'].\
            track_end_index, None) 
                            
        self.assertEqual(self.test_cuesheet.tracks['01'].\
            track_number, 2)   
        self.assertEqual(self.test_cuesheet.tracks['01'].\
            track_enumeration, 'TRACK 01') 
        self.assertEqual(self.test_cuesheet.tracks['01'].\
            track_performer, 'Jane Doe')  
        self.assertEqual(self.test_cuesheet.tracks['01'].\
            track_file_name, '0001 - book.mp3')   
        self.assertEqual(self.test_cuesheet.tracks['01'].\
            track_title, 'Dedication') 
        self.assertEqual(self.test_cuesheet.tracks['01'].\
            track_start_index, '00:09:42') 
        self.assertEqual(self.test_cuesheet.tracks['01'].\
            track_end_index, None) 

        self.assertEqual(self.test_cuesheet.tracks['02'].\
            track_number, 3)   
        self.assertEqual(self.test_cuesheet.tracks['02'].\
            track_enumeration, 'TRACK 02') 
        self.assertEqual(self.test_cuesheet.tracks['02'].\
            track_performer, 'Jane Doe')  
        self.assertEqual(self.test_cuesheet.tracks['02'].\
            track_file_name, '0002 - book.mp3')   
        self.assertEqual(self.test_cuesheet.tracks['02'].\
            track_title, 'Prologue') 
        self.assertEqual(self.test_cuesheet.tracks['02'].\
            track_start_index, '00:19:24') 
        self.assertEqual(self.test_cuesheet.tracks['02'].\
            track_end_index, None) 


class test_CueTrack(unittest.TestCase):
    

    def setUp(self):
        self.test_cuetrack = CueTrack()
         
    def tearDown(self):
        del self.test_cuetrack   
    
    def test_cuesheet_attributes(self):
        self.assertTrue(hasattr(self.test_cuetrack, 
                                'track_number'))
        self.assertTrue(hasattr(self.test_cuetrack, 
                                'track_enumeration'))    
        self.assertTrue(hasattr(self.test_cuetrack, 
                                'track_performer'))    
        self.assertTrue(hasattr(self.test_cuetrack, 
                                'track_file_name'))    
        self.assertTrue(hasattr(self.test_cuetrack, 
                                'track_title'))  
        self.assertTrue(hasattr(self.test_cuetrack, 
                                'track_start_index'))    
        self.assertTrue(hasattr(self.test_cuetrack, 
                                'track_end_index'))  