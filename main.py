from portability import resource_path
import pathlib
from cue_reader import CueSheet
from audio_cutter import AudioCutter


from loggingSettings import logger_wrapper, logger_initialization
from pydub import AudioSegment


def start():
  #  AudioSegment.converter = "/usr/bin/snap/"
    
    cue_sheet = CueSheet()
    cue_sheet.sheet_reader_liner()
    cue_sheet.add_ending_time()
    audio_cutter = AudioCutter()
    audio_cutter.cut_audio_tracks(list(cue_sheet.tracks.values()))
    # album = AudioSegment.from_file("szczelina.mp3", "mp3")
    pass


def main():
    logger = logger_initialization("pydub.converter")   
    # logger = logging.getLogger("pydub.converter")
    # logger.setLevel(logging.INFO)
    # formatter = logging.Formatter(
    #     '%(levelname)s: %(asctime)s: %(process)s: %(funcName)s: %(message)s')

    # stream_handler = logging.StreamHandler()
    # file_handler = logging.FileHandler('logfile.log')
    # file_handler.setFormatter(formatter)
    # logger.addHandler(stream_handler)
    start()


if __name__ == "__main__":
    main()