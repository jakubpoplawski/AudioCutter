import os
from dotenv import load_dotenv 

from argumentParser import ArgumentParser
from cueReader import CueSheet
from audioCutter import AudioCutter
from ipScanner import IPScanner
from audioSender import SFTPClient

from loggingSettings import logger_initialization


load_dotenv()

def main():     
    logger = logger_initialization("ffmpeg_audio_cutter.log") 
 
    logger.info('Parsing arguments.') 
    
    arguement_parser = ArgumentParser()
        
    (local_file_path, local_cue_sheet_path, local_artwork_path, 
    local_cut_files_path, remote_file_path) = \
        arguement_parser.parse_arguments()

    logger.info('Extracting data from cue sheet file.')
    
    cue_sheet = CueSheet(local_cue_sheet_path)
    cue_sheet.sheet_reader_liner()
    cue_sheet.add_ending_time()

    logger.info('Cutting audio file according to the cue sheet file.')
    
    audio_cutter = AudioCutter(local_file_path, local_cut_files_path)
    audio_cutter.cut_audio_tracks_ffmpeg(
        list(cue_sheet.tracks.values()), local_artwork_path)
    
    logger.info('Scanning wi-fi network for available local addresses.')
    
    ip_scanner = IPScanner(
                        os.environ.get('PORT'),
                        os.environ.get('IP_RANGE'),
                        os.environ.get('REGEX_IP_FILTER'))        

    retived_IPs = ip_scanner.scan_ips()

    logger.info('Identifying the address from the collected list.')
 
    sftp_client = SFTPClient(
                            os.environ.get('PORT'),
                            os.environ.get('REMOTE_USER'),
                            os.environ.get('PASSWORD'),
                            retived_IPs)
    
    sftp_client.ssh_scan_connect()

    logger.info('Uploading data to the connected device.')
 
    sftp_client.ssh_upload_album(list(cue_sheet.tracks.values()), 
                                  local_cut_files_path, 
                                  remote_file_path, 
                                  cue_sheet.title,
                                  local_artwork_path)

    logger.info('Disconnecting from the device.')
    
    sftp_client.ssh_disconnect()


if __name__ == "__main__":
    main()