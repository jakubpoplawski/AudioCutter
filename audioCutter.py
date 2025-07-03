import ffmpeg
import pathlib

from portability import resource_path
from loggingSettings import logger_wrapper

class AudioCutter():
    def __init__(self, source_path, output_path):
        self.source_path = pathlib.Path(resource_path(source_path))
        self.output_path = pathlib.Path(resource_path(output_path))   

    @logger_wrapper
    def time_to_miliseconds(self, input_time):
        try:
            temp_time = list(map(int, input_time.split(":")))
        except ValueError as e:
            raise e
        # CUE time is in MM:SS:FF format
        return temp_time[0] * 60 * 1000 + \
               temp_time[1] * 1000 + \
               temp_time[2] * (4 / 3)

    @logger_wrapper
    def time_to_seconds(self, input_time):
        try:
            temp_time = list(map(int, input_time.split(":")))
        except ValueError as e:
            raise e
        # CUE time is in MM:SS:FF format - 75 frames in 1 second
        return temp_time[0] * 60 + temp_time[1] + temp_time[2] / 75

    @logger_wrapper         
    def cut_audio_tracks_ffmpeg(self, track_list):
        track_list_length = len(track_list)
        for i in range(track_list_length):
            metadata_list = [f"title={track_list[i].track_title}",
                             f"artist={track_list[i].track_performer}", 
            f"track={track_list[i].track_number}/{track_list_length}"]
            metadata_dict = {f"metadata:g:{i}": e for i, e in enumerate(
                metadata_list)}
            
            fragment_start_index = self.time_to_seconds(
                track_list[i].track_start_index)
            
            if i == len(track_list)-1:
                audio_input = ffmpeg.input(self.source_path, 
                                           ss=fragment_start_index)        
            else:
                fragment_end_index = self.time_to_seconds(
                    track_list[i].track_end_index)
                audio_input = ffmpeg.input(self.source_path, 
                            ss=fragment_start_index, 
                            t=fragment_end_index-fragment_start_index)
            audio_output = ffmpeg.output(audio_input, 
                f"{self.output_path}/{track_list[i].track_file_name}", 
                acodec="copy", **metadata_dict)
            
            audio_output.run()
