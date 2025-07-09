import ffmpeg
import pathlib
import logging

from portability import resource_path
from loggingSettings import logger_wrapper

logger = logging.getLogger(__name__)

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
        return (temp_time[0] * 60 * 1000 
               + temp_time[1] * 1000 
               + temp_time[2] * (4 / 3))

    @logger_wrapper
    def time_to_seconds(self, input_time):
        try:
            temp_time = list(map(int, input_time.split(":")))
        except ValueError as e:
            raise e
        # CUE time is in MM:SS:FF format - 75 frames in 1 second
        return temp_time[0] * 60 + temp_time[1] + temp_time[2] / 75

    @logger_wrapper         
    def cut_audio_tracks_ffmpeg(self, track_list, 
                                artwork_file_path=None):
        track_list_length = len(track_list)
        for i in range(track_list_length):
            track_path = \
                f"{self.output_path}/{track_list[i].track_file_name}"
            if pathlib.Path(track_path).is_file():
                logger.info(f"File {track_list[i].track_file_name} \
                    already exists.")
            else:
                metadata_list = \
                    [f"title={track_list[i].track_title}",
                    f"artist={track_list[i].track_performer}", 
                    "track=" \
                    f"{track_list[i].track_number}/{track_list_length}"]
                metadata_dict = \
                    {f"metadata:g:{i}": e for i, e in enumerate(
                        metadata_list)}
                
                if artwork_file_path != None:
                    metadata_dict['metadata:s:v'] = \
                        f'file={artwork_file_path}'
                
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
                audio_output = ffmpeg.output(audio_input, track_path, 
                    id3v2_version=3, acodec="copy", **metadata_dict)
                
                audio_output.run()
