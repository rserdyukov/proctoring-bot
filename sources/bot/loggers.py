"""
Logger installer implementation module.
"""
import logging


class LogInstaller:
    """
    Logger installer class allows to configure requested logger.
    """

    INFO = logging.INFO
    WARN = logging.WARN
    ERROR = logging.ERROR
    DEBUG = logging.DEBUG

    log_formats = {"default": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"}

    @staticmethod
    def add_format(other: dict):
        """
        Allows adding and using specified logger print format in the future.

        :param other: Format dictionary
        :type other: :obj:`dict`
        """
        LogInstaller.log_formats.update(other)

    @staticmethod
    def get_logger(package_name: str, format_name: str, level: int) -> logging.Logger:
        """
        Allows adding and using specified custom logger in the future.

        :param package_name: Logger placeholder class name
        :type package_name: :obj:`str`

        :param format_name: Logging message format
        :type format_name: :obj:`str`

        :param level: Logging level in (INFO, WARN, ERROR, DEBUG)
        :type level: :obj:`int

        :return: Returns configured logger instance.
        :rtype: :obj:`logging.Logger`
        """
        logger = logging.getLogger(package_name)
        logging.basicConfig(
            level=level,
            format=LogInstaller.log_formats.get(format_name),
        )
        return logger

    @staticmethod
    def get_default_logger(package_name: str, level: int) -> logging.Logger:
        """
        Allows adding and using standard logger in the future.

        :param package_name: Logger placeholder class name
        :type package_name: :obj:`str`

        :param level: Logging level in (INFO, WARN, ERROR, DEBUG)
        :type level: :obj:`int`

        :return: Returns configured logger instance.
        :rtype: :obj:`logging.Logger`
        """
        return LogInstaller.get_logger(package_name, "default", level)
