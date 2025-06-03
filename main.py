import os
import sys
import pathlib
from dotenv import load_dotenv, find_dotenv 


from portability import resource_path


from cue_reader import CueSheet
from audio_cutter import AudioCutter
from audio_sender import SFTPClient


from loggingSettings import logger_wrapper, logger_initialization

local_file_path = '/home/jakub/Documents/PythonScripts/AudioCutter/.test_files/expected_files/'
remote_file_path = 'Audiobooks/'


load_dotenv()



def main():


    logger = logger_initialization("ffmpeg.converter")   
    cue_sheet = CueSheet()
    cue_sheet.sheet_reader_liner()
    cue_sheet.add_ending_time()
    # audio_cutter = AudioCutter()
    # audio_cutter.cut_audio_tracks_ffmpeg(list(cue_sheet.tracks.values()))

    sftmp_client = SFTPClient(os.environ.get("HOST_IP"), 
                              os.environ.get('PORT'),
                              os.environ.get('REMOTE_USER'),
                              os.environ.get('PASSWORD'))
    sftmp_client.ssh_connect()
    
    sftmp_client.ssh_upload_album(list(cue_sheet.tracks.values()), local_file_path, remote_file_path, cue_sheet.title)
    
    sftmp_client.ssh_disconnect()


if __name__ == "__main__":
    main()