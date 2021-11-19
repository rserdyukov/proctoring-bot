from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from bot.loggers import LogInstaller
from bot.modules.chains.main.main_handlers_chain import MainHandlersChain
from bot.modules.handlers_chain import HandlersChain
from bot.modules.handlers_registrar import HandlersRegistrar as Registrar


class AuthStates(StatesGroup):
    fio = State()
    group = State()
    subgroup = State()


class AuthHandlersChain(HandlersChain):
    _logger = LogInstaller.get_default_logger(__name__, LogInstaller.DEBUG)

    @staticmethod
    @Registrar.callback_query_handler(text="auth")
    async def start_handler(query: types.CallbackQuery):
        AuthHandlersChain._logger.debug(f"Start auth conversation state")
        await AuthStates.fio.set()

        await Registrar.bot.send_message(query.from_user.id, "Введите ваше ФИО.")

    @staticmethod
    @Registrar.message_handler(commands=["cancel"], state="*")
    async def cancel_handler(message: types.Message, state: FSMContext):
        current_state = await state.get_state()
        if current_state is None:
            return

        AuthHandlersChain._logger.debug(f"Cancel auth conversation state {current_state}")

        await state.finish()
        await message.reply("Спасибо за регистрацию.")

    @staticmethod
    @Registrar.message_handler(lambda message: len(message.text.split(" ")) != 3, state=AuthStates.fio)
    async def wrong_fio_handler(message: types.Message):
        return await message.reply("Вы неправильно ввели имя! (Укажите полное ФИО.)")

    @staticmethod
    @Registrar.message_handler(lambda message: len(message.text.split(" ")) == 3, state=AuthStates.fio)
    async def process_fio_handler(message: types.Message, state: FSMContext):
        await AuthStates.next()
        await state.update_data(auth={"name": message.text})

        await message.reply("Укажите номер группы.")

    @staticmethod
    @Registrar.message_handler(state=AuthStates.group)
    async def process_group_handler(message: types.Message, state: FSMContext):
        await AuthStates.next()

        data = await state.get_data()
        data["auth"]["group"] = message.text
        await state.update_data(auth=data["auth"])

        await message.reply("Укажите номер подгруппы.")

    @staticmethod
    @Registrar.message_handler(state=AuthStates.subgroup)
    async def process_subgroup_handler(message: types.Message, state: FSMContext):
        AuthHandlersChain._logger.debug(f"Finite auth conversation state")
        await AuthStates.next()

        data = await state.get_data()
        auth_data = data["auth"]
        auth_data["subgroup"] = message.text
        await state.update_data(auth=auth_data)

        await message.reply(f"Спасибо за регистрацию.\n\n{MainHandlersChain.get_info(data)}")
