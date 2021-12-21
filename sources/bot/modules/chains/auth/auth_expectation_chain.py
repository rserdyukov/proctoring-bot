import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup
from aiogram.types import ChatType
from aiogram.types import InlineKeyboardMarkup

from ....loggers import LogInstaller
from ...handlers_chain import HandlersChain
from ...handlers_registrar import HandlersRegistrar as Registrar
from ...keyboard.keyboard import KeyboardBuilder


class AuthExpectationHandlersChain(HandlersChain):
    _logger = LogInstaller.get_default_logger(__name__, LogInstaller.DEBUG)

    @staticmethod
    async def _check_user_registration_completing(message: types.Message, state: FSMContext) -> bool:
        data = await state.get_data()
        username = message.from_user.username

        if data.get("auth") != {}:
            text = f"Регистрация @{username} пройдена успешно."
            await Registrar.bot.send_message(chat_id=message.chat.id, text=text)

            AuthExpectationHandlersChain._logger.debug(f"User @{username} have been registered")
            return True

        return False


    @staticmethod
    async def _ask_for_user_registration(message: types.Message, state: FSMContext):
        AuthExpectationHandlersChain._logger.debug(f"Start register timer at {Registrar.bot.register_timeout} minutes")
        timeout = Registrar.bot.register_timeout * 60

        while timeout > 0:
            is_registered = await AuthExpectationHandlersChain._check_user_registration_completing(message, state)
            if is_registered:
                break

            await asyncio.sleep(1)
            timeout -= 1


    @staticmethod
    async def _send_user_not_registered(message: types.Message):
        username = message.from_user.username
        chat_id = message.chat.id

        text = f"Регистрация не была пройдена, @{username} удалён из чата."
        await Registrar.bot.send_message(chat_id=chat_id, text=text)

        wait_before_kick_timeout = 5
        await asyncio.sleep(wait_before_kick_timeout)
        await message.chat.kick(user_id=message.from_user.id)

        AuthExpectationHandlersChain._logger.debug(f"User @{username} kicked")


    @staticmethod
    async def wait_registration(message: types.Message, state: FSMContext, not_registered):
        if not_registered:
            await AuthExpectationHandlersChain._ask_for_user_registration(message, state)

        data = await state.get_data()

        if data.get("auth") == {}:
            AuthExpectationHandlersChain._send_user_not_registered(message)
