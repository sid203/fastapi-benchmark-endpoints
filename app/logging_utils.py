import os
from logging import Logger, basicConfig, config, getLogger
from os.path import dirname as parent_dir
from typing import Any, Dict, Optional

from envyaml import EnvYAML

default_logging_config = os.path.join(parent_dir(parent_dir(__file__)), "config/logging.yml")


class WithLogging:
    """
    Logging Base Class to be used for extending classes that needs to log messages
    """

    @property
    def logger(self) -> Logger:
        """
        Create logger

        :return: default logger
        """
        name_logger = str(self.__class__).replace("<class '", "").replace("'>", "")
        return getLogger(name_logger)


def config_from_file(file: str = default_logging_config) -> None:
    config_as_dict: Dict[Any, Any] = EnvYAML(file)
    return config.dictConfig(config_as_dict)


def get_default_logger(level: str) -> Logger:
    basicConfig(level=level)
    return getLogger()


def get_named_logger(name: Optional[str]) -> Logger:
    return getLogger(name=name)
