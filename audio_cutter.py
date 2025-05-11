from pydub import AudioSegment
from portability import resource_path
import pathlib
import subprocess

# command = ["ffmpeg", "-i", input_path, "-ss", str(start_time), "-t", str(duration), output_path]

class AudioCutter():
    def __init__(self):
        self.source_path = pathlib.Path(resource_path('.test_files/source_files/skaza.mp3'))
        self.output_path = pathlib.Path(resource_path('.test_files/expected_files/'))        


    def time_to_miliseconds(self, input_time):
        temp_time = list(map(int, input_time.split(":")))
        return temp_time[0] * 60 * 1000 + temp_time[1] * 1000 + temp_time[2]

    def cut_audio_tracks(self, track_list):
        # command = AudioSegment.from_mp3(self.source_path)
        # album = subprocess.run(command, check=True)
        album = AudioSegment.from_mp3(self.source_path)
        for i in range(len(track_list)):
            fragment_start_index = self.time_to_miliseconds(track_list[i].track_start_index)
            if i == len(track_list)-1:
                fragment_end_index = len(album)               
            else:
                fragment_end_index = self.time_to_miliseconds(track_list[i].track_end_index)
            extract = album[fragment_start_index:fragment_end_index]

            extract.export(f"{self.output_path}/{track_list[i].track_file_name}", format="mp3")
