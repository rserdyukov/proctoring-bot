"""
Bot students and teachers authorization handlers chain implementation module.
"""
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from ....loggers import LogInstaller
from ...chains.main.main_handlers_chain import MainHandlersChain
from ...handlers_chain import HandlersChain
from ...handlers_registrar import HandlersRegistrar as Registrar


class AuthStates(StatesGroup):
    """
    Bot students and teachers authorization handlers chain states class implementation.
    """

    fio = State()
    group = State()
    subgroup = State()


class AuthHandlersChain(HandlersChain):
    """
    Bot students and teachers authorization handlers chain class implementation.
    """

    _logger = LogInstaller.get_default_logger(__name__, LogInstaller.DEBUG)

    @staticmethod
    @Registrar.callback_query_handler(text="auth")
    async def start_handler(query: types.CallbackQuery):
        """
        Asks student or teacher name in registration process.

        Note: Handler may be started if authorization button has been pressed.

        :param query: Callback query message
        :type query: :obj:`types.CallbackQuery`
        """
        AuthHandlersChain._logger.debug("Start auth conversation state")
        await AuthStates.fio.set()

        await Registrar.bot.send_message(query.from_user.id, "Введите ваше ФИО.")

    @staticmethod
    @Registrar.message_handler(lambda message: len(message.text.split(" ")) != 3, state=AuthStates.fio)
    async def wrong_fio_handler(message: types.Message):
        """
        Notifies student or teacher about incorrect name format.

        Note: Handler may be started after incorrect name input by student or teacher.

        :param message: User message data
        :type message: :obj:`types.Message`
        """
        return await message.answer("Вы неправильно ввели имя! (Укажите полное ФИО.)")

    @staticmethod
    @Registrar.message_handler(lambda message: len(message.text.split(" ")) == 3, state=AuthStates.fio)
    async def process_fio_handler(message: types.Message, state: FSMContext):
        """
        Asks student or teacher group in registration process.

        Note: Handler may be started after correct name input by student or teacher.

        :param message: User message data
        :type message: :obj:`types.Message`

        :param state: User state machine context
        :type state: :obj:`FSMContext`
        """
        await AuthStates.next()
        await state.update_data(auth={"name": message.text})

        await message.answer("Укажите номер группы.")

    @staticmethod
    @Registrar.message_handler(state=AuthStates.group)
    async def process_group_handler(message: types.Message, state: FSMContext):
        """
        Asks student subgroup in registration process.

        Note: Handler may be started after group input by student.

        :param message: User message data
        :type message: :obj:`types.Message`

        :param state: User state machine context
        :type state: :obj:`FSMContext`
        """
        await AuthStates.next()

        data = await state.get_data()
        data["auth"]["group"] = message.text
        await state.update_data(auth=data["auth"])

        await message.answer("Укажите номер подгруппы.")

    @staticmethod
    @Registrar.message_handler(state=AuthStates.subgroup)
    async def process_subgroup_handler(message: types.Message, state: FSMContext):
        """
        Greets student for registration process.

        Note: Handler may be started after subgroup input by student.

        :param message: User message data
        :type message: :obj:`types.Message`

        :param state: User state machine context
        :type state: :obj:`FSMContext`
        """
        AuthHandlersChain._logger.debug("Finite auth conversation state")
        await AuthStates.next()

        data = await state.get_data()
        auth_data = data["auth"]
        auth_data["subgroup"] = message.text
        await state.update_data(auth=auth_data)

        await message.answer(f"Спасибо за регистрацию.\n\n{MainHandlersChain.get_info(data)}")
