import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext

from ....loggers import LogInstaller
from ...handlers_chain import HandlersChain
from ...handlers_registrar import HandlersRegistrar as Registrar
from ...keyboard.keyboard import KeyboardBuilder


class AuthExpectationHandlersChain(HandlersChain):
    _logger = LogInstaller.get_default_logger(__name__, LogInstaller.DEBUG)

    async def _send_user_about_registration_completing(self, message: types.Message):
        username = message.from_user.username

        text = f"Регистрация @{username} пройдена успешно."
        await Registrar.bot.send_message(chat_id=message.chat.id, text=text)

        AuthExpectationHandlersChain._logger.debug(f"User @{username} have been registered")

    async def _ask_for_user_registration(self, message: types.Message, state: FSMContext):
        AuthExpectationHandlersChain._logger.debug(f"Start register timer at {Registrar.bot.register_timeout} minutes")
        timeout = Registrar.bot.register_timeout * 60

        while timeout > 0:
            data = await state.get_data()
            if data.get("auth") != {}:
                await self._send_user_about_registration_completing(message)
                break

            await asyncio.sleep(1)
            timeout -= 1

    async def _kick_user(self, message: types.Message):
        username = message.from_user.username
        chat_id = message.chat.id

        text = f"Регистрация не была пройдена, @{username} удалён из чата."
        await Registrar.bot.send_message(chat_id=chat_id, text=text)

        wait_before_kick_timeout = 5
        await asyncio.sleep(wait_before_kick_timeout)
        await message.chat.kick(user_id=message.from_user.id)

        AuthExpectationHandlersChain._logger.debug(f"User @{username} kicked")

    async def wait_registration(self, message: types.Message, state: FSMContext, not_registered):
        if not_registered:
            await self._ask_for_user_registration(message, state)

        data = await state.get_data()

        if data.get("auth") == {}:
            await self._kick_user(message)
