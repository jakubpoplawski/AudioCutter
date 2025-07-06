import os
import sys
import pathlib
from dotenv import load_dotenv 
import argparse

from cueReader import CueSheet
from audioCutter import AudioCutter
from ipScanner import IPScanner
from audioSender import SFTPClient

from portability import resource_path
from loggingSettings import logger_initialization

# local_file_path = '.test_files/source_files/skaza.mp3'
# local_cue_sheet_path = '.test_files/source_files/skaza.cue'
# local_cut_files_path = pathlib.Path(resource_path('.test_files/expected_files/'))
# local_cut_files_path = '.test_files/expected_files/'
# remote_file_path = 'Audiobooks/'

# sys.argv = ['main.py', '-f='+local_file_path,'-s='+local_cue_sheet_path, 
#             '-c='+str(local_cut_files_path), '-r='+remote_file_path]


load_dotenv()



def main():
    

    logger = logger_initialization("ffmpeg_audio_cutter.log") 
 
    logger.info('Parsing arguments.') 
      
    parser = argparse.ArgumentParser(
        description="""A script to read a *.cue file and cut an 
        *.mp3 audiobook, and send it via SSH to a a remote device.""")
    parser.add_argument('-f','--file', 
                        help='Path to the audiobook file', 
                        required=True)
    parser.add_argument('-s','--sheet', 
                        help='Path to the cue sheet file', 
                        required=True)
    parser.add_argument('-c','--cut', 
                        help='Path to store cut mp3s locally', 
                        required=True)
    parser.add_argument('-r','--remote', 
                        help='Path to remote target directory', 
                        required=True)    
    
    args = parser.parse_args()

    local_file_path = args.file
    local_cue_sheet_path = args.sheet
    local_cut_files_path = pathlib.Path(resource_path(args.cut))
    remote_file_path = args.remote
    
    if not pathlib.Path(local_file_path).is_file():
        logger.info("The local mp3 file doesn't exist in specified \
            directory.")
        raise SystemExit(1)
    
    if not pathlib.Path(local_cue_sheet_path).is_file():
        logger.info("The local cue sheet file doesn't exist in \
            specified directory.")
        raise SystemExit(1)

    if not pathlib.Path(local_cut_files_path).is_dir():
        logger.info("The target file path to save cut files doesn't \
            exist in specified directory.")
        raise SystemExit(1)

    logger.info('Extracting data from cue sheet file.')
    
    cue_sheet = CueSheet(local_cue_sheet_path)
    cue_sheet.sheet_reader_liner()
    cue_sheet.add_ending_time()

    logger.info('Cutting audio file according to the cue sheet file.')
    
    audio_cutter = AudioCutter(local_file_path, local_cut_files_path)
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
                                  local_cut_files_path, 
                                  remote_file_path, 
                                  cue_sheet.title)

    logger.info('Disconnecting from the device.')
    
    sftmp_client.ssh_disconnect()


if __name__ == "__main__":
    main()