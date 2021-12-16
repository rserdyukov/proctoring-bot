"""
Config interface module.
"""
from abc import ABCMeta, abstractmethod


class BaseConfig:
    """
    Config interface.
    """

    __metaclass__ = ABCMeta

    def get_bot_option(self, option: str) -> str:
        """
        Gets bot options value.

        :param option: Config option
        :type option: :obj:`str`

        :return: Returns bot option value.
        :rtype: :obj:`str`
        """
        raise NotImplementedError

    def get_chat_option(self, option: str) -> str:
        """
        Gets chat options value.

        :param option: Config option
        :type option: :obj:`str`

        :return: Returns chat option value.
        :rtype: :obj:`str`
        """
        raise NotImplementedError

    def get_spreadsheet_option(self, option: str) -> str:
        """
        Gets spreadsheet options value.

        :param option: Config option
        :type option: :obj:`str`

        :return: Returns spreadsheet option value.
        :rtype: :obj:`str`
        """
        raise NotImplementedError
