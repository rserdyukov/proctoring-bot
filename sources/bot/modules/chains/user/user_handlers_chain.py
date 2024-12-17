"""
Bot user handlers chain implementation module.
"""

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup
from aiogram.types import ChatType
from aiogram.types import InlineKeyboardMarkup

from ....loggers import LogInstaller
from ...handlers_chain import HandlersChain
from ...handlers_registrar import HandlersRegistrar as Registrar
from ...keyboard.keyboard import KeyboardBuilder
from ..auth.auth_expectation_chain import AuthExpectationHandlersChain


class UserKeyboardsBuilder:
    """
    Bot user handlers chain keyboard builder class implementation.
    """


class UserHandlersChain(HandlersChain):
    """
    Bot User handlers chain class implementation.
    """

    _logger = LogInstaller.get_default_logger(__name__, LogInstaller.DEBUG)
