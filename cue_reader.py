from portability import resource_path
import pathlib
import re


class CueSheet():
    
    def __init__(self):
        self.performer = None
        self.title = None
        self.album_file_name = None
        self.tracks = {}
        
    # def sheet_reader(self):    
    #     with open(pathlib.Path(resource_path('.test_files/source_files/szczelina.cue'))) as cue_file:
    #         content = cue_file.read()
 
    #         album_performer = re.findall('^PERFORMER .(.*)\"\s', content)
    #         self.performer = album_performer[0]

    #         album_title = re.findall('\nTITLE .(.*)\"\s', content)
    #         self.title = album_title[0]

    #         album_file_name = re.findall('\nFILE .(.*)\"\s', content)
    #         self.album_file_name = album_file_name[0]

    #         track_pattern = '(TRACK [0-9]*).AUDIO\s{3}PERFORMER..(.*)\"\s{3}REM..(.*)\".[0-9]*\s{3}TITLE..(.*)\"\s{3}INDEX 01 (.*)'
    #         track_list = re.findall(track_pattern, content)
    #         for match in track_list:
    #             current_track = match[0]
    #             self.tracks[current_track] = CueTrack()
    #             self.tracks[current_track].performer = match[1]      
    #             self.tracks[current_track].track_file_name = match[2]                                 
    #             self.tracks[current_track].title = match[3]      
    #             self.tracks[current_track].start_index = match[4]   
 
    def eval_album_performer(self, input_line):
        try:
            album_performer = re.match('^PERFORMER .(.*)\"\s', input_line)
            self.performer = album_performer.groups(0)[0]
        except AttributeError:
            pass   
 
    def eval_album_title(self, input_line):
        try:
            album_title = re.match('^TITLE .(.*)\"\s', input_line)
            self.title = album_title.groups(0)[0]
        except AttributeError:
            pass   
 
    def eval_album_file_name(self, input_line):
        try:
            album_file_name = re.match('^FILE .(.*)\"\s', input_line)
            self.album_file_name = album_file_name.groups(0)[0]
        except AttributeError:
            pass  


    def eval_track_beginning(self, input_line):
        try:
            track_number = re.match('\t(TRACK.*) AUDIO\s', input_line)
            current_track_name = track_number.groups(0)[0]
            self.tracks[current_track_name] = CueTrack()
            return current_track_name
        except AttributeError:
            pass   
 
 
    def eval_track_performer(self, current_track_name, input_line):
        try:
            track_performer = re.match('\s{2}PERFORMER .(.*)\"\s', input_line)
            self.tracks[current_track_name].track_performer = track_performer.groups(0)[0]
        except AttributeError:
            pass   
 
    def eval_track_file_name(self, current_track_name, input_line):
        try:
            track_file_name = re.match('\s{2}REM .(.*)\"\s', input_line)
            self.tracks[current_track_name].track_file_name = track_file_name.groups(0)[0]
        except AttributeError:
            pass   
 
    def eval_track_title(self, current_track_name, input_line):
        try:
            track_title = re.match('\s{2}TITLE .(.*)\"\s', input_line)
            self.tracks[current_track_name].track_title = track_title.groups(0)[0]
        except AttributeError:
            pass  
 
    def eval_track_start_index(self, current_track_name, input_line):
        try:
            track_start_index = re.match('\s{2}INDEX 01 (\d{1,}\:\d{2}\:\d{2})\s', input_line)
            self.tracks[current_track_name].track_start_index = track_start_index.groups(0)[0]
        except AttributeError:
            pass  
 
  
    def sheet_reader_liner(self):
        current_track_name = None  
        with open(pathlib.Path(resource_path('.test_files/source_files/szczelina.cue'))) as cue_file:
            for line in cue_file:
                if not self.performer:
                    self.eval_album_performer(line)  
                if not self.title:               
                    self.eval_album_title(line)                 
                if not self.album_file_name:
                    self.eval_album_file_name(line)
                    
                if re.match('\t(TRACK.*) AUDIO\s', line):
                    current_track_name = self.eval_track_beginning(line)
                    self.tracks[current_track_name] = CueTrack()
                    self.tracks[current_track_name].track_number = current_track_name
                if current_track_name:
                    if not self.tracks[current_track_name].track_performer:
                        self.eval_track_performer(current_track_name, line)                     
                    if not self.tracks[current_track_name].track_file_name:
                        self.eval_track_file_name(current_track_name, line)            
                    if not self.tracks[current_track_name].track_title:
                        self.eval_track_title(current_track_name, line)                          
                    if not self.tracks[current_track_name].track_start_index:
                        self.eval_track_start_index(current_track_name, line)   
                                            
class CueTrack():

    def __init__(self):
        self.track_number = None
        self.track_performer = None
        self.track_file_name = None
        self.track_title = None
        self.track_start_index = None  
    