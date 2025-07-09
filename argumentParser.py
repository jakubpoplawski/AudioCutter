import logging
import argparse
import pathlib

from portability import resource_path
from loggingSettings import logger_wrapper


logger = logging.getLogger(__name__)

class ArgumentParser():
    
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="""A script to read a *.cue file and cut an 
                        *.mp3 audiobook, and send it via SSH to 
                        a remote device.""")


    @logger_wrapper
    def parse_arguments(self):       
        self.parser.add_argument('-f','--file', 
                            help='Path to the audiobook file', 
                            required=True)
        self.parser.add_argument('-s','--sheet', 
                            help='Path to the cue sheet file', 
                            required=True)
        self.parser.add_argument('-a','--artwork', 
                            help='Path to the artwork file', 
                            required=False)   
        self.parser.add_argument('-c','--cut', 
                            help='Path to store cut mp3s locally', 
                            required=True)
        self.parser.add_argument('-r','--remote', 
                            help='Path to remote target directory', 
                            required=True)    
    
        args = self.parser.parse_args()
        
        file_path = str(pathlib.Path(args.file))
        cue_sheet_path = str(pathlib.Path(args.sheet))
        artwork_path = str(pathlib.Path(args.artwork)) \
                        if args.artwork else None 
        output_folder_path = str(pathlib.Path(args.cut))
        remote_folder_path = str(pathlib.Path(args.remote))
        

        self.validate_arguments(file_path, cue_sheet_path, 
                                output_folder_path, artwork_path)
            
        return (file_path, cue_sheet_path, artwork_path,
            output_folder_path, remote_folder_path)

    @logger_wrapper
    def validate_arguments(self, file_path, cue_sheet_path, 
                           output_folder_path, artwork_path=None):
        if not pathlib.Path(file_path).is_file():
            logger.info("The local mp3 file doesn't exist in specified \
                directory.")
            raise SystemExit(1)
        
        if not pathlib.Path(file_path).suffix == '.mp3':
            logger.info("The provided source file is not a *.mp3 file.")
            raise SystemExit(1)        
        
        if not pathlib.Path(cue_sheet_path).is_file():
            logger.info("The local cue sheet file doesn't exist in \
                specified directory.")
            raise SystemExit(1)
        
        if not pathlib.Path(cue_sheet_path).suffix == '.cue':
            logger.info("The provided sheet file is not a *.cue file.")
            raise SystemExit(1)          

        if not pathlib.Path(output_folder_path).is_dir():
            logger.info("The target file path to save cut files \
                doesn't exist in specified directory.")
            raise SystemExit(1)
        
        if artwork_path != None:
            if not pathlib.Path(artwork_path).is_file():
                logger.info("The local artwork file doesn't exist in \
                    specified directory.")
                raise SystemExit(1)            
            
            if pathlib.Path(artwork_path).suffix \
            not in ('.jpeg', '.jpg', '.png'):
                logger.info(
                    "The provided artwork file is not a *.jpg, *jpeg \
                    or *.png file.")
                raise SystemExit(1)           