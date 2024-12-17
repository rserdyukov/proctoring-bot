"""
Bot user handlers chain implementation module.
"""

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from ....loggers import LogInstaller
from ...handlers_chain import HandlersChain
from ...handlers_registrar import HandlersRegistrar as Registrar
from ...chains.main.main_handlers_chain import MainHandlersChain


class ChangeStudentInformationStates(StatesGroup):
    """
    Bot students changing handlers chain states class implementation.
    """

    fio = State()
    group = State()
    subgroup = State()


class ChangeStudentInformationHandlersChain(HandlersChain):
    """
    Bot User handlers chain class implementation.
    """

    _logger = LogInstaller.get_default_logger(__name__, LogInstaller.DEBUG)

    
    @staticmethod
    @Registrar.callback_query_handler(text="edit_student_info")
    async def start_handler(query: types.CallbackQuery):
        """
        Asks student name in changing process.

        Note: Handler may be started if changing button has been pressed.

        :param query: Callback query message
        :type query: :obj:`types.CallbackQuery`
        """
        ChangeStudentInformationHandlersChain._logger.debug("Start changing conversation state")
        await ChangeStudentInformationStates.fio.set()

        await Registrar.bot.send_message(query.from_user.id, "Введите ваше ФИО.")

    @staticmethod
    @Registrar.message_handler(lambda message: len(message.text.split(" ")) != 3, state=ChangeStudentInformationStates.fio)
    async def wrong_fio_handler(message: types.Message):
        """
        Notifies student or teacher about incorrect name format.

        Note: Handler may be started after incorrect name input by student or teacher.

        :param message: User message data
        :type message: :obj:`types.Message`
        """
        return await message.answer("Вы неправильно ввели имя! (Укажите полное ФИО.)")

    @staticmethod
    @Registrar.message_handler(lambda message: len(message.text.split(" ")) == 3, state=ChangeStudentInformationStates.fio)
    async def process_fio_handler(message: types.Message, state: FSMContext):
        """
        Asks student group in changing process.

        Note: Handler may be started after correct name input by student.

        :param message: User message data
        :type message: :obj:`types.Message`

        :param state: User state machine context
        :type state: :obj:`FSMContext`
        """
        await ChangeStudentInformationStates.next()
        await state.update_data(change={"name": message.text})

        await message.answer("Укажите номер группы.")

    @staticmethod
    @Registrar.message_handler(state=ChangeStudentInformationStates.group)
    async def process_group_handler(message: types.Message, state: FSMContext):
        """
        Asks student subgroup in registration process.

        Note: Handler may be started after group input by student.

        :param message: User message data
        :type message: :obj:`types.Message`

        :param state: User state machine context
        :type state: :obj:`FSMContext`
        """
        await ChangeStudentInformationStates.next()

        data = await state.get_data()
        data["change"]["group"] = message.text
        await state.update_data(change=data["change"])

        await message.answer("Укажите номер подгруппы.")

    @staticmethod
    @Registrar.message_handler(state=ChangeStudentInformationStates.subgroup)
    async def process_subgroup_handler(message: types.Message, state: FSMContext):
        """
        Greets student for registration process.

        Note: Handler may be started after subgroup input by student.

        :param message: User message data
        :type message: :obj:`types.Message`

        :param state: User state machine context
        :type state: :obj:`FSMContext`
        """
        ChangeStudentInformationHandlersChain._logger.debug("Finite changing conversation state")
        await ChangeStudentInformationStates.next()

        data = await state.get_data()
        change_data = data["change"]
        change_data["subgroup"] = message.text
        await state.update_data(auth=change_data)

        await message.answer(f"Спасибо за регистрацию.\n\n{MainHandlersChain.get_info(data)}")
