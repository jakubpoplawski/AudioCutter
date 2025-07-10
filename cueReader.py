import pathlib
import re
import logging

from loggingSettings import logger_wrapper
from portability import resource_path

logger = logging.getLogger(__name__)

class CueSheet():
    
    def __init__(self, file_location):
        """A class to store functions to collect data from the *.cue 
        file and store it its parameters.

        Parameters:
            file_location (Path class): Location of the *.cue file.
            performer (str): Album performer.  
            title (str): Title of the album.
            album_file_name (str): File name with the extension.
            tracks (dict): Dictionary of the collected tracks. 
            exec_plan (dict): Dictionary with the regexes to collect 
                              the line data from the *.cue file.                                              
        """
        self.file_location = pathlib.Path(resource_path(file_location))
        self.performer = None
        self.title = None
        self.album_file_name = None
        self.tracks = {}
        self.exec_plan = {
            # album
            "performer": '^PERFORMER .(.*)\"\s', 
            "title": '^TITLE .(.*)\"\s',                                     
            "file": 'FILE .(.*)\"\s',          
            # track header
            "track_beginning": '\tTRACK.(\d*) AUDIO\s',            
            # track
            "track_performer": '\s{2}PERFORMER .(.*)\"\s', 
            "track_file_name": '\s{2}REM .(.*)\"\s',                                     
            "track_title": '\s{2}TITLE .(.*)\"\s',
            "track_start_index": 
                '\s{2}INDEX 01 (\d{1,}\:\d{2}\:\d{2})\s?'                                            
        }

 
    @logger_wrapper              
    def eval_line(self, regex_pattern, input_line):
        """The function checks a file line with a regex pattern and 
        returns data if match was found.

        Args:
            regex_pattern (str): Regex pattern.
            input_line (str): Line evaluated in the *.cue file.   
        
        Returns:
            string (str): Match if cought with the regex pattern.           
        """  
        try:
            match = re.match(regex_pattern, input_line)
            if regex_pattern == self.exec_plan["track_beginning"]:
                current_track = match.groups(0)[0]
                self.tracks[current_track] = CueTrack()
                return current_track, self.tracks[current_track]                
            return match.groups(0)[0]
        except AttributeError as e:
            pass

    @logger_wrapper  
    def sheet_reader_liner(self):
        """The function opens the *.cue file and controls the flow of 
        data extraction.

        Args:
            None
        
        Returns:
            None        
        """  
        current_track = None  
        with open(self.file_location) as cue_file:
            for line in cue_file:
                if not self.performer:
                    self.performer = self.eval_line(
                        self.exec_plan["performer"], line)  
                if not self.title:               
                    self.title = self.eval_line(
                        self.exec_plan["title"], line)                 
                if not self.album_file_name:
                    self.album_file_name = self.eval_line(
                        self.exec_plan["file"], line)

                if re.match(self.exec_plan["track_beginning"], line):
                    current_track, self.tracks[current_track] = \
                        self.eval_line(
                            self.exec_plan["track_beginning"], line)
                    self.tracks[current_track].track_enumeration = \
                        f"TRACK {current_track}"
                    self.tracks[current_track].track_number = \
                        int(current_track) + 1  
                                            
                if current_track:
                    if not self.tracks[current_track].track_performer:
                        self.tracks[current_track].track_performer = \
                            self.eval_line(
                                self.exec_plan["track_performer"], line)                     
                    if not self.tracks[current_track].track_file_name:
                        self.tracks[current_track].track_file_name = \
                            self.eval_line(
                                self.exec_plan["track_file_name"], line)            
                    if not self.tracks[current_track].track_title:
                        self.tracks[current_track].track_title = \
                            self.eval_line(
                                self.exec_plan["track_title"], line)                           
                    if not self.tracks[current_track].track_start_index:
                        self.tracks[current_track].track_start_index = \
                            self.eval_line(
                                self.exec_plan["track_start_index"], 
                                line)

    @logger_wrapper   
    def add_ending_time(self):
        """The function adds to the collected tracks metadata 
        the information on the ending timestaps of the cut files.

        Args:
            None
        
        Returns:
            None        
        """ 
        prev_track = None
        for track in self.tracks.values():
            if track.track_enumeration == "TRACK 00":
                prev_track = track
                continue
            prev_track.track_end_index = track.track_start_index
            prev_track = track

            
                                     
class CueTrack():

    def __init__(self):
        """A class to store the collected data from the *.cue 
        on specific tracks.

        Parameters:
            track_number (int): Track number starting from 1.
            track_enumeration (int): Cue track number starting from 
                                     TRACK 00.
            track_performer (str): Perfomer of the each track.
            track_file_name (str): File name with the extension.
            track_title (str): Title of each section.  
            track_start_index (str): Starting timestamp of a track in 
                                     MM:SS:FF cue format.   
            track_end_index (str): Ending timestamp of a track in 
                                   MM:SS:FF cue format.                                                  
        """
        self.track_number = None
        self.track_enumeration = None
        self.track_performer = None
        self.track_file_name = None
        self.track_title = None
        self.track_start_index = None  
        self.track_end_index = None  
        

    