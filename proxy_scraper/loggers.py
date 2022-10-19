import logging

import os

from proxy_scraper.Utils import BASE_PATH


class Utilities:
    DATA_DIR_PATH = os.path.join(BASE_PATH, "data")

    @staticmethod
    def get_app_dir() -> str:
        """
        Gets the app directory where all data related to the script is stored

        :return:
        """

        app_dir = os.path.join(os.path.expanduser("~"), ".generator_mail")
        if not os.path.isdir(app_dir):
            # If the app data dir does not exist create it
            os.mkdir(app_dir)
        return app_dir


class CustomFileHandler(logging.FileHandler):
    """
    Allows us to log to the app directory
    """

    def __init__(self, file_name="app.log", mode="a"):
        log_file_path = os.path.join(Utilities.get_app_dir(), file_name)
        super(CustomFileHandler, self).__init__(log_file_path, mode)


def load_logging_config(logger_name) -> None:
    """
    Load logging configuration

    :return: None
    """

    my_logger = logging.getLogger(logger_name)
    my_logger.setLevel(logging.INFO)

    # File handler
    file_handler = CustomFileHandler()
    log_format = "%(asctime)s::%(name)s::%(levelname)s::%(module)s: %(message)s"
    formatter = logging.Formatter(fmt=log_format)
    file_handler.setFormatter(formatter)
    my_logger.addHandler(file_handler)

    # Basic format for streamhandler
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    my_logger.addHandler(stream_handler)


def get_logger(logger_name="Gmail-Generator") -> logging.Logger:
    """
    Convenience method to load the app logger

    :return: An instance of the app logger
    """
    load_logging_config(logger_name)
    return logging.getLogger(logger_name)
