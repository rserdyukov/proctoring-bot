import validators
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import (
    StatesGroup,
    State,
)

from ....loggers import LogInstaller
from ...handlers_chain import HandlersChain
from ...handlers_registrar import HandlersRegistrar as Registrar


class WorkStates(StatesGroup):
    waiting_for_link = State()


class WorkHandlersChain(HandlersChain):
    _logger = LogInstaller.get_default_logger(__name__, LogInstaller.DEBUG)

    @staticmethod
    @Registrar.message_handler(commands=["lab"], state="*")
    async def lab_start_handler(message: types.Message):
        WorkHandlersChain._logger.debug(f"Start lab conversation state")

        await message.answer("Отправьте ссылку на лабораторную работу.")
        await WorkStates.waiting_for_link.set()

    @staticmethod
    @Registrar.callback_query_handler(text="lab")
    async def lab_start_handler(query: types.CallbackQuery):
        WorkHandlersChain._logger.debug(f"Start lab conversation state")

        await Registrar.bot.send_message(query.from_user.id, "Отправьте ссылку на лабораторную работу.")
        await WorkStates.waiting_for_link.set()

    @staticmethod
    @Registrar.message_handler(state=WorkStates.waiting_for_link)
    async def lab_link_send_handler(message: types.Message, state: FSMContext):
        if validators.url(str(message.text)):
            await state.update_data(works=message.text)
            await message.answer("Ссылка успешно добавлена.")
            WorkHandlersChain._logger.debug(f"Finite lab conversation state")
            await state.finish()
        else:
            await message.answer("Пожалуйста, отправьте действительную ссылку.")
