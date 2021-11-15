from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from bot.loggers import LogInstaller
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
        await state.update_data(fio=message.text)

        await message.reply("Укажите номер группы.")

    @staticmethod
    @Registrar.message_handler(state=AuthStates.group)
    async def process_group_handler(message: types.Message, state: FSMContext):
        await AuthStates.next()
        await state.update_data(group=message.text)

        await message.reply("Укажите номер подгруппы.")

    @staticmethod
    @Registrar.message_handler(state=AuthStates.subgroup)
    async def process_subgroup_handler(message: types.Message, state: FSMContext):
        AuthHandlersChain._logger.debug(f"Finite auth conversation state")
        await AuthStates.next()
        await state.update_data(subgroup=message.text)

        data = await state.get_data()
        fio = data["fio"]
        group = data["group"]
        subgroup = data["subgroup"]

        await message.reply(
            "Спасибо за регистрацию.\n\n" f"Информация о Вас:\nФИО: {fio}\nГруппа: {group}\nПодгруппа: {subgroup}\n"
        )

    @staticmethod
    @Registrar.message_handler(commands=["info"])
    async def get_info_handler(message: types.Message, state: FSMContext):
        data = await state.get_data()
        fio = data.get("fio")
        group = data.get("group")
        subgroup = data.get("subgroup")

        await state.finish()
        await message.reply(
            f"Информация о Вас:\nФИО: {fio}\nГруппа: {group}\nПодгруппа: {subgroup}\n"
        )
