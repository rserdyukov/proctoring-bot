from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup
from aiogram.types import ChatType

from bot.loggers import LogInstaller
from bot.modules.handlers_chain import HandlersChain
from bot.modules.handlers_registrar import HandlersRegistrar as Registrar
from bot.modules.keyboard.keyboard import KeyboardBuilder


class MainStates(StatesGroup):
    pass


class MainKeyboardsBuilder:
    @staticmethod
    def get_private_start_keyboard():
        return KeyboardBuilder.get_inline_keyboard_markup(
            [
                {
                    "Пройти регистрацию": "auth",
                },
            ]
        )

    @staticmethod
    def get_info_keyboard():
        return KeyboardBuilder.get_inline_keyboard_markup(
            [
                {
                    "Посмотреть информацию": "info",
                },
            ]
        )


class MainHandlersChain(HandlersChain):
    _logger = LogInstaller.get_default_logger(__name__, LogInstaller.DEBUG)

    @staticmethod
    @Registrar.message_handler(chat_type=ChatType.GROUP, commands="start")
    async def start_handler(message: types.Message, state: FSMContext):
        MainHandlersChain._logger.debug(f"Start main group conversation state")

        data = await state.get_data()
        if data.get("auth") is None or len(data.get("auth").keys()) != 3:
            bot = Registrar.bot
            me = await bot.get_me()
            text = f"Привет, {message.from_user.first_name}!\nПройдите, пожалуйста, регистрацию\n\n@{me.username}"
        else:
            text = f"Привет, {message.from_user.first_name}\nВы уже зарегестрированы"

        await message.reply(text)

    @staticmethod
    @Registrar.message_handler(chat_type=ChatType.PRIVATE, commands="start")
    async def start_handler(message: types.Message, state: FSMContext):
        MainHandlersChain._logger.debug(f"Start main private conversation state")

        await state.update_data(username=message.from_user.username)
        data = await state.get_data()
        if data.get("auth") is None or len(data.get("auth").keys()) != 3:
            text = f"Привет, {message.from_user.first_name}!\nНачнём регистрацию\n"
            keyboard_markup = MainKeyboardsBuilder.get_private_start_keyboard()
        else:
            text = f"Привет, {message.from_user.first_name}\nВы уже зарегестрированы"
            keyboard_markup = MainKeyboardsBuilder.get_info_keyboard()

        await message.reply(text, reply_markup=keyboard_markup)

    @staticmethod
    @Registrar.message_handler(commands=["info"])
    async def get_info_handler(message: types.Message, state: FSMContext):
        data = await state.get_data()
        await message.reply(MainHandlersChain.get_info(data))

    @staticmethod
    @Registrar.callback_query_handler(text="info")
    async def get_info_handler(query: types.CallbackQuery, state: FSMContext):
        data = await state.get_data()
        await query.message.reply(MainHandlersChain.get_info(data))

    @staticmethod
    def get_info(data) -> str:
        auth_data = data["auth"]

        if data["type"] == "student":
            name = auth_data.get("name")
            group = auth_data.get("group")
            subgroup = auth_data.get("subgroup")

            return f"Информация о Вас:\nФИО: {name}\nГруппа: {group}\nПодгруппа: {subgroup}\n"
        elif data["type"] == "teacher":
            name = auth_data.get("name")

            return f"Информация о Вас:\nФИО: {name}\n"
