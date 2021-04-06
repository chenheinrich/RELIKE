import logging
import os


def set_log_level(logger):
    if "LOG_LEVEL" in os.environ:
        level = os.environ["LOG_LEVEL"].upper()
        exec("logger.setLevel(logging.{})".format(level))
    else:
        logger.setLevel(logging.INFO)


def setup_logger(name):
    logger = logging.getLogger(name)
    set_log_level(logger)
    logging.basicConfig()
    return logger


logger = setup_logger('relike')


def class_logger(obj):
    return setup_logger(type(obj).__name__)


def file_logger(file):
    this_file = os.path.splitext(os.path.basename(file))[0]
    logger = setup_logger(' ' + this_file + ' ')
    return logger
