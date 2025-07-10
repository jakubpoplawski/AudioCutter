import unittest
import sys

from unittest.mock import patch, MagicMock

patch('loggingSettings.logger_wrapper', lambda x: x).start()
   
from argumentParser import ArgumentParser



class test_argumentParser(unittest.TestCase):
    
    def setUp(self):
        self.test_argumentparser = ArgumentParser()

    def tearDown(self):
        del self.test_argumentparser   
         
         
    def test_argumentparser_attributes(self):
        self.assertTrue(hasattr(self.test_argumentparser, 'parser'))
        
    def test_parse_arguments_with_artwork(self):
        sys.argv = ['main.py', 
            '-f=/home/Documents/the-book/the-book.mp3',
            '-s=/home/Documents/the-book/the-book.cue', 
            '-a=/home/Documents/the-book/the-book.jpg', 
            '-c=/home/Documents/the-book/output-files/', 
            '-r=Audiobooks/']
        
        with patch("pathlib.Path.__str__") as mock_str:
            mock_str.side_effect = \
                ['/home/Documents/the-book/the-book.mp3',
                 '/home/Documents/the-book/the-book.cue',
                 '/home/Documents/the-book/the-book.jpg',
                 '/home/Documents/the-book/output-files/',
                 'Audiobooks/']
            
            self.test_argumentparser.validate_arguments = MagicMock()
           
            parsed = self.test_argumentparser.parse_arguments()
            
            self.test_argumentparser.\
                validate_arguments.assert_called_with(
                    '/home/Documents/the-book/the-book.mp3', 
                    '/home/Documents/the-book/the-book.cue', 
                    '/home/Documents/the-book/output-files/',
                    '/home/Documents/the-book/the-book.jpg')  
                   
            self.assertEqual(parsed[0], 
                             '/home/Documents/the-book/the-book.mp3')
            self.assertEqual(parsed[1], 
                             '/home/Documents/the-book/the-book.cue')
            self.assertEqual(parsed[2], 
                             '/home/Documents/the-book/the-book.jpg')
            self.assertEqual(parsed[3], 
                             '/home/Documents/the-book/output-files/')           
            self.assertEqual(parsed[4], 'Audiobooks/') 


    def test_parse_arguments_no_artwork(self):
        sys.argv = ['main.py', 
            '-f=/home/Documents/the-book/the-book.mp3',
            '-s=/home/Documents/the-book/the-book.cue', 
            '-c=/home/Documents/the-book/output-files/', 
            '-r=Audiobooks/']
        
        with patch("pathlib.Path.__str__") as mock_str:
            mock_str.side_effect = \
                ['/home/Documents/the-book/the-book.mp3',
                 '/home/Documents/the-book/the-book.cue',
                 '/home/Documents/the-book/output-files/',
                 'Audiobooks/']
            
            self.test_argumentparser.validate_arguments = MagicMock()
           
            parsed = self.test_argumentparser.parse_arguments()
            
            self.test_argumentparser.\
                validate_arguments.assert_called_with(
                    '/home/Documents/the-book/the-book.mp3', 
                    '/home/Documents/the-book/the-book.cue', 
                    '/home/Documents/the-book/output-files/',
                    None)              
            
            self.assertEqual(parsed[0], 
                             '/home/Documents/the-book/the-book.mp3')
            self.assertEqual(parsed[1], 
                             '/home/Documents/the-book/the-book.cue')
            self.assertEqual(parsed[2], None)
            self.assertEqual(parsed[3], 
                             '/home/Documents/the-book/output-files/')           
            self.assertEqual(parsed[4], 'Audiobooks/') 

    def test_validate_arguments_with_artwork_wrong_format_error(self):
        with patch("pathlib.Path.is_file") as mock_is_file:
            with self.assertRaises(SystemExit):
                mock_is_file.side_effect = [True, True, True]   
                        
                self.test_argumentparser.validate_arguments(        
                            '/home/Documents/the-book/the-book.wav',
                            '/home/Documents/the-book/the-book.cue',
                            '/home/Documents/the-book/output-files/',
                            '/home/Documents/the-book/the-book.jpg')

    def test_validate_arguments_with_artwork_wrong_path_error(self):
        with patch("pathlib.Path.is_file") as mock_is_file:
            with self.assertRaises(SystemExit):
                mock_is_file.side_effect = [False, True, True]   
                        
                self.test_argumentparser.validate_arguments(        
                            '/home/Documents/the-book/the-book.mp3',
                            '/home/Documents/the-book/the-book.cue',
                            '/home/Documents/the-book/output-files/',
                            '/home/Documents/the-book/the-book.jpg')     

    def test_validate_arguments_with_artwork_not_dir_error(self):
        with patch("pathlib.Path.is_file") as mock_is_file:
            with patch("pathlib.Path.is_dir") as mock_is_dir:
                with self.assertRaises(SystemExit):
                    mock_is_file.side_effect = [True, True, True]
                    mock_is_dir.return_value = False   
                         
                    self.test_argumentparser.validate_arguments(        
                            '/home/Documents/the-book/the-book.mp3',
                            '/home/Documents/the-book/the-book.cue',
                            '/home/Documents/the-book/output-files/',
                            '/home/Documents/the-book/the-book.jpg')          

    def test_validate_arguments_with_wrong_artwork_error(self):
        with patch("pathlib.Path.is_file") as mock_is_file:
            with patch("pathlib.Path.is_dir") as mock_is_dir:
                with self.assertRaises(SystemExit):
                    mock_is_file.side_effect = [True, True, True]
                    mock_is_dir.return_value = True  
                         
                    self.test_argumentparser.validate_arguments(        
                            '/home/Documents/the-book/the-book.mp3',
                            '/home/Documents/the-book/the-book.cue',
                            '/home/Documents/the-book/output-files/',
                            '/home/Documents/the-book/the-book.svg')         
        
    def test_validate_arguments_no_artwork(self):
        with patch("pathlib.Path.is_file") as mock_is_file:
            with patch("pathlib.Path.is_dir") as mock_is_dir:
                mock_is_file.side_effect = [True, True, True]
                mock_is_dir.return_value = True      
                  
                self.test_argumentparser.validate_arguments(         
                        '/home/Documents/the-book/the-book.mp3',
                        '/home/Documents/the-book/the-book.cue',
                        '/home/Documents/the-book/output-files/')
                
                self.assertEqual(mock_is_file.call_count, 2)
                self.assertEqual(mock_is_dir.call_count, 1)
                