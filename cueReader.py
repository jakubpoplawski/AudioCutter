import pathlib
import re

from loggingSettings import logger_wrapper
from portability import resource_path
import logging

logger = logging.getLogger(__name__)


class CueSheet():
    
    def __init__(self, file_location):
        self.file_location = pathlib.Path(resource_path(file_location))
        self.performer = None
        self.title = None
        self.album_file_name = None
        self.tracks = {}
        self.execution_plan = {
            # album
            "performer": '^PERFORMER .(.*)\"\s', 
            "title": '^TITLE .(.*)\"\s',                                     
            "file": 'FILE .(.*)\"\s',          
            # track
            "track_beginning": '\tTRACK.(\d*) AUDIO\s',            
            # "track_beginning": '\tTRACK.(*) AUDIO\s',
            "track_performer": '\s{2}PERFORMER .(.*)\"\s', 
            "track_file_name": '\s{2}REM .(.*)\"\s',                                     
            "track_title": '\s{2}TITLE .(.*)\"\s',
            "track_start_index": '\s{2}INDEX 01 (\d{1,}\:\d{2}\:\d{2})\s'                                            
        }

 
    @logger_wrapper              
    def eval_line(self, regex_pattern, input_line):
        try:
            match = re.match(regex_pattern, input_line)
            if regex_pattern == self.execution_plan["track_beginning"]:
                current_track_number = match.groups(0)[0]
                self.tracks[current_track_number] = CueTrack()
                return current_track_number, self.tracks[current_track_number]                
            return match.groups(0)[0]
        except AttributeError as e:
            pass

  
    @logger_wrapper  
    def sheet_reader_liner(self):
        current_track_name = None  
        with open(self.file_location) as cue_file:
            for line in cue_file:
                if not self.performer:
                    self.performer = self.eval_line(
                        self.execution_plan["performer"], line)  
                if not self.title:               
                    self.title = self.eval_line(
                        self.execution_plan["title"], line)                 
                if not self.album_file_name:
                    self.album_file_name = self.eval_line(
                        self.execution_plan["file"], line)

                if re.match(self.execution_plan["track_beginning"], line):
                    current_track_name, self.tracks[current_track_name] = \
                        self.eval_line(
                            self.execution_plan["track_beginning"], line)
                    self.tracks[current_track_name].track_enumeration = \
                        f"TRACK {current_track_name}"
                    self.tracks[current_track_name].track_number = \
                        int(current_track_name) + 1  
                                            
                if current_track_name:
                    if not self.tracks[current_track_name].track_performer:
                        self.tracks[current_track_name].track_performer = \
                        self.eval_line(
                            self.execution_plan["track_performer"], line)                     
                    if not self.tracks[current_track_name].track_file_name:
                        self.tracks[current_track_name].track_file_name = \
                        self.eval_line(
                            self.execution_plan["track_file_name"], line)            
                    if not self.tracks[current_track_name].track_title:
                        self.tracks[current_track_name].track_title = \
                        self.eval_line(
                            self.execution_plan["track_title"], line)                           
                    if not self.tracks[current_track_name].track_start_index:
                        self.tracks[current_track_name].track_start_index = \
                        self.eval_line(
                            self.execution_plan["track_start_index"], line)

    @logger_wrapper   
    def add_ending_time(self):
        prev_track = None
        for track in self.tracks.values():
            if track.track_enumeration == "TRACK 00":
                prev_track = track
                continue
            prev_track.track_end_index = track.track_start_index
            prev_track = track

            
                                     
class CueTrack():

    def __init__(self):
        self.track_number = None
        self.track_enumeration = None
        self.track_performer = None
        self.track_file_name = None
        self.track_title = None
        self.track_start_index = None  
        self.track_end_index = None  
        

    