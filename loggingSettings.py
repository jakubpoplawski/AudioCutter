import logging.config
import pathlib
from portability import resource_path

def logger_initialization(log_name):
    """The function initializes the logger instance and adds its 
    parameters.

    Args:
        log_name (str): The name of the log file with its extension.
    
    Returns:
        logger (instance): Logger class instance.           
    """  
    global logger

    logger = logging.getLogger("ffmpeg.converter")
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(levelname)s: %(asctime)s: '\
        '%(process)s: %(funcName)s: %(message)s')

    stream_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(pathlib.Path(
        resource_path(f'Settings/{log_name}')))
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger


def logger_wrapper(func):
    """The function is used as a wrapper to handle information retrival 
    from the called functions to the logger instance.

    Args:
        func (function): The name of the wrapped function.
    
    Returns:
        log_wrapper (function): Function wrapped with logger functions 
                                passing info to the logger instance.           
    """  
    def log_wrapper(*args):
        logger.info(
            f'{func.__name__} section started with arguments: {args}.')
        try:
            result = func(*args)
        except Exception as e:
            logger.error(e)
            logger.info(f'{func.__name__} section ended with an error.')
            return None
        logger.info(f'{func.__name__} section ended.')
        return result
    
    return log_wrapper