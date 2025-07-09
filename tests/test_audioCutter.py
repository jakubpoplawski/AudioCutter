import unittest
import ffmpeg
import pathlib

from unittest.mock import patch, MagicMock, mock_open

patch('loggingSettings.logger_wrapper', lambda x: x).start()
   
from audioCutter import AudioCutter

from cueReader import CueSheet, CueTrack


class test_audioCutter(unittest.TestCase):
    
    def setUp(self):
        with patch("builtins.open", 
                   mock_open(read_data="data")) as mock_file:
            self.test_audiocutter = AudioCutter('tests/dummy.mp3', 
                                                'tests/dummy_outputs/')
        
        self.test_cuesheet = CueSheet('tests/dummy_cue.cue')
        self.test_cuesheet.sheet_reader_liner()
        self.test_cuesheet.add_ending_time()
        
    def tearDown(self):
        del self.test_audiocutter   
        del self.test_cuesheet
         
    
    def test_audiocutter_attributes(self):
        self.assertTrue(hasattr(self.test_audiocutter, 'source_path'))
        self.assertTrue(hasattr(self.test_audiocutter, 'output_path'))   
        
    def test_time_to_miliseconds(self):
        self.assertEqual(
            self.test_audiocutter.time_to_miliseconds("00:09:42"), 9056)
        with self.assertRaises(ValueError):
            self.test_audiocutter.time_to_miliseconds("MM:09:42") 
        
    def test_time_to_seconds(self):
        self.assertEqual(
            self.test_audiocutter.time_to_seconds("00:09:42"), 9.56)
        with self.assertRaises(ValueError):
            self.test_audiocutter.time_to_seconds("00:MM:42")

    def test_cut_audio_tracks_ffmpeg_no_artwork(self):
            ffmpeg_mock = ffmpeg
            ffmpeg_mock.input = MagicMock(return_value='InputMock')
            ffmpeg_mock.output = MagicMock()
            ffmpeg_mock.output.run = MagicMock(return_value=True)                  
            self.test_audiocutter.cut_audio_tracks_ffmpeg(
                    list(self.test_cuesheet.tracks.values()))            
            ffmpeg_mock.input.assert_called()
            
            expected_metadata_01 = {'metadata:g:0':'title=Start', 
                                    'metadata:g:1':'artist=Jane Doe', 
                                    'metadata:g:2':'track=1/3'}
            ffmpeg_mock.output.assert_any_call('InputMock', 
                str(pathlib.Path(
                './tests/dummy_outputs/0000 - book.mp3').absolute()), 
                id3v2_version=3, acodec='copy',
                **expected_metadata_01)     
            
            expected_metadata_02 = {'metadata:g:0':'title=Dedication', 
                                    'metadata:g:1':'artist=Jane Doe', 
                                    'metadata:g:2':'track=2/3'}
            ffmpeg_mock.output.assert_any_call('InputMock', 
                str(pathlib.Path(
                './tests/dummy_outputs/0001 - book.mp3').absolute()), 
                id3v2_version=3, acodec='copy',
                **expected_metadata_02)        
            
            expected_metadata_03 = {'metadata:g:0':'title=Prologue', 
                                    'metadata:g:1':'artist=Jane Doe', 
                                    'metadata:g:2':'track=3/3'}
            ffmpeg_mock.output.assert_any_call('InputMock', 
                str(pathlib.Path(
                './tests/dummy_outputs/0002 - book.mp3').absolute()), 
                id3v2_version=3, acodec='copy',
                **expected_metadata_03) 

    def test_cut_audio_tracks_ffmpeg_with_artwork(self):
            ffmpeg_mock = ffmpeg
            ffmpeg_mock.input = MagicMock(return_value='InputMock')
            ffmpeg_mock.output = MagicMock()
            ffmpeg_mock.output.run = MagicMock(return_value=True)   
            dummy_artwork_path = \
                str(pathlib.Path('./tests/artwork.jpg').absolute())             
            self.test_audiocutter.cut_audio_tracks_ffmpeg(
                list(self.test_cuesheet.tracks.values()),
                dummy_artwork_path)     
            ffmpeg_mock.input.assert_called()       

            expected_metadata_01 = {'metadata:g:0':'title=Start', 
                            'metadata:g:1':'artist=Jane Doe', 
                            'metadata:g:2':'track=1/3',
                            'metadata:s:v':f'file={dummy_artwork_path}'}
            ffmpeg_mock.output.assert_any_call('InputMock', 
                str(pathlib.Path(
                './tests/dummy_outputs/0000 - book.mp3').absolute()), 
                id3v2_version=3, acodec='copy',
                **expected_metadata_01)  

            expected_metadata_02 = {'metadata:g:0':'title=Dedication', 
                            'metadata:g:1':'artist=Jane Doe', 
                            'metadata:g:2':'track=2/3',
                            'metadata:s:v':f'file={dummy_artwork_path}'}
            ffmpeg_mock.output.assert_any_call('InputMock', 
                str(pathlib.Path(
                './tests/dummy_outputs/0001 - book.mp3').absolute()), 
                id3v2_version=3, acodec='copy',
                **expected_metadata_02)  

            expected_metadata_03 = {'metadata:g:0':'title=Prologue', 
                            'metadata:g:1':'artist=Jane Doe', 
                            'metadata:g:2':'track=3/3',
                            'metadata:s:v':f'file={dummy_artwork_path}'}
            ffmpeg_mock.output.assert_any_call('InputMock', 
                str(pathlib.Path(
                './tests/dummy_outputs/0002 - book.mp3').absolute()), 
                id3v2_version=3, acodec='copy',
                **expected_metadata_03)  