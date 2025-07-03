import os
import pathlib
from dotenv import load_dotenv 

from cueReader import CueSheet
from audioCutter import AudioCutter
from ipScanner import IPScanner
from audioSender import SFTPClient

from portability import resource_path
from loggingSettings import logger_initialization

local_file_path = pathlib.Path(resource_path('.test_files/expected_files/'))
remote_file_path = 'Audiobooks/'


load_dotenv()



def main():


    logger = logger_initialization("ffmpeg_audio_cutter.log")   
    
    logger.info('Extracting data from cue sheet file.')
    
    cue_sheet = CueSheet('.test_files/source_files/skaza.cue')
    cue_sheet.sheet_reader_liner()
    cue_sheet.add_ending_time()

    logger.info('Cutting audio file according to the cue sheet file.')
    
    audio_cutter = AudioCutter('.test_files/source_files/skaza.mp3', 
                               '.test_files/expected_files/')
    audio_cutter.cut_audio_tracks_ffmpeg(
        list(cue_sheet.tracks.values()))
    
    logger.info('Scanning wi-fi network for available local addresses.')
    
    ip_scanner = IPScanner(
                        os.environ.get('PORT'),
                        os.environ.get('IP_RANGE'),
                        os.environ.get('REGEX_IP_FILTER'))        

    retived_IPs = ip_scanner.scan_ips()

    logger.info('Identifying the address from the collected list.')
 
    sftmp_client = SFTPClient(
                            os.environ.get('PORT'),
                            os.environ.get('REMOTE_USER'),
                            os.environ.get('PASSWORD'),
                            retived_IPs)
    
    sftmp_client.ssh_scan_connect()

    logger.info('Uploading data to the connected device.')
 
    sftmp_client.ssh_upload_album(list(cue_sheet.tracks.values()), 
                                  local_file_path, 
                                  remote_file_path, 
                                  cue_sheet.title)

    logger.info('Disconnecting from the device.')
    
    sftmp_client.ssh_disconnect()


if __name__ == "__main__":
    main()