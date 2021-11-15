from aiogram import types
from aiogram.dispatcher.filters.state import StatesGroup

from bot.loggers import LogInstaller
from bot.modules.handlers_chain import HandlersChain
from bot.modules.handlers_registrar import HandlersRegistrar as Registrar
from bot.modules.keyboard.keyboard import KeyboardBuilder


class MainStates(StatesGroup):
    pass


class MainKeyboardsBuilder:
    @staticmethod
    def get_start_keyboard():
        return KeyboardBuilder.get_inline_keyboard_markup(
            [
                {
                    "Пройти регистрацию": "auth",
                },
            ]
        )


class MainHandlersChain(HandlersChain):
    _logger = LogInstaller.get_default_logger(__name__, LogInstaller.DEBUG)

    @staticmethod
    @Registrar.message_handler(commands='start')
    async def start_cmd_handler(message: types.Message):
        MainHandlersChain._logger.debug(f"Start main conversation state")
        keyboard_markup = MainKeyboardsBuilder.get_start_keyboard()

        # todo: Add check if user is registered
        await message.reply(
            f"Привет, {message.from_user.first_name}!"
            f"\nПройдите, пожалуйста, регистрацию.", reply_markup=keyboard_markup)
