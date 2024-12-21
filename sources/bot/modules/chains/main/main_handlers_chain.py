"""
Bot main handlers chain implementation module.
"""
import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ChatType
from aiogram.types import InlineKeyboardMarkup

from ....loggers import LogInstaller
from ...handlers_chain import HandlersChain
from ...handlers_registrar import HandlersRegistrar as Registrar
from ...keyboard.keyboard import KeyboardBuilder
from ..auth.auth_expectation_chain import AuthExpectationHandlersChain
from ....storage.spreadsheet.works.works_spreadsheet_handler import WorksSpreadsheetHandler


class MainStates(StatesGroup):
    """
    Bot main handlers chain states class implementation.
    """
    SELECT_STUDENT_FOR_GRADE = State()
    SET_LAB_GRADE = State()


class MainKeyboardsBuilder:
    """
    Bot main handlers chain keyboard builder class implementation.
    """

    @staticmethod
    def get_private_start_keyboard() -> InlineKeyboardMarkup:
        """
        Gets keyboard to send message to private user chat.

        :return: Returns inline keyboard markup.
        :rtype: :obj:`InlineKeyboardMarkup`
        """
        return KeyboardBuilder.get_inline_keyboard_markup(
            [
                {
                    "Пройти регистрацию": "auth",
                },
            ]
        )

    @staticmethod
    def get_info_keyboard() -> InlineKeyboardMarkup:
        """
        Gets keyboard to send information about user message to chat.

        :return: Returns inline keyboard markup.
        :rtype: :obj:`InlineKeyboardMarkup`
        """
        return KeyboardBuilder.get_inline_keyboard_markup(
            [
                {
                    "Посмотреть информацию": "info",
                },
                {
                    "Отправить лабораторную работу": "lab",
                },
                {
                    "Оценить лабораторную работу": "set_grade",
                },
            ]
        )


class MainHandlersChain(HandlersChain):
    """
    Bot main handlers chain class implementation.
    """

    _logger = LogInstaller.get_default_logger(__name__, LogInstaller.DEBUG)
    #ID таблицы(works)
    work_spreadsheet_id = "183vR-Xle6pIBZshZWv_7Uqj4c1X0DjpNHMvTWGVjwFU"
    #Пути к файлу с токенами(work)
    path_to_work_token = "/home/miko/Projects/proctoring-bot/sources/tokens/works_token.json"

    @staticmethod
    async def _start_routine(message: types.Message, state: FSMContext):
        username = message.from_user.username
        greeting = f"Привет, {message.from_user.first_name} (@{username}).\n"
        bot = await Registrar.bot.get_me()

        await state.update_data(username=username)
        data = await state.get_data()
        data_size = len(data.get("auth").keys())
        not_registered = data_size != 3 and data_size != 1

        if not_registered:
            MainHandlersChain._logger.debug(f"User @{username} is not registered")
            text = f"{greeting}Вы не зарегистрированы.\nПройти регистрацию: @{bot.username}."
            keyboard_markup = MainKeyboardsBuilder.get_private_start_keyboard()
        else:
            MainHandlersChain._logger.debug(f"User @{username} is registered")
            text = f"{greeting}Вы уже зарегистрированы.\nПодробности: @{bot.username}."
            keyboard_markup = MainKeyboardsBuilder.get_info_keyboard()

        return text, keyboard_markup, not_registered

    @staticmethod
    @Registrar.message_handler(content_types=types.ContentTypes.NEW_CHAT_MEMBERS)
    async def start_handler(message: types.Message, state: FSMContext):
        """
        Asks user ro start registration process or speaks about that he is registered.

        :param message: User message data
        :type message: :obj:`types.Message`

        :param state: User state machine context
        :type state: :obj:`FSMContext`
        """
        MainHandlersChain._logger.debug("Start main group conversation state")
        text, _, not_registered = await MainHandlersChain._start_routine(message, state)

        await Registrar.bot.send_message(chat_id=message.chat.id, text=text)
        await AuthExpectationHandlersChain().wait_registration(message, state, not_registered)

    @staticmethod
    @Registrar.message_handler(commands=["start"], chat_type=ChatType.PRIVATE)
    async def start_handler(message: types.Message, state: FSMContext):
        """
        Starts dialog with user by 'start' command. Shows to user main keyboard to choose action.
        Send to user registration state message.

        :param message: User message data
        :type message: :obj:`types.Message`

        :param state: User state machine context
        :type state: :obj:`FSMContext`
        """
        MainHandlersChain._logger.debug("Start main private conversation state")
        text, keyboard_markup, _ = await MainHandlersChain._start_routine(message, state)
        text = text.replace(f"(@{message.from_user.username})", "")
        await message.answer(text, reply_markup=keyboard_markup)

    @staticmethod
    @Registrar.message_handler(commands=["cancel"], state="*")
    async def cancel_handler(message: types.Message, state: FSMContext):
        """
        Cancels conversation by 'cancel' command.

        Note: Handler may be started everywhere.

        :param message: User message data
        :type message: :obj:`types.Message`

        :param state: User state machine context
        :type state: :obj:`FSMContext`
        """
        current_state = await state.get_state()
        if current_state is None:
            return

        MainHandlersChain._logger.debug(f"Cancel {current_state} conversation state")

        await state.finish()
        await message.answer("Действие отменено")

    @staticmethod
    @Registrar.message_handler(commands=["info"])
    async def get_info_handler(message: types.Message, state: FSMContext):
        """
        Sends to user information: username, name, group and subgroup by 'info' command.

        :param message: User message data
        :type message: :obj:`types.Message`

        :param state: User state machine context
        :type state: :obj:`FSMContext`
        """
        data = await state.get_data()
        await message.answer(MainHandlersChain.get_info(data))

    @staticmethod
    @Registrar.callback_query_handler(text="info")
    async def get_info_handler(query: types.CallbackQuery, state: FSMContext):
        """
        Sends to user information: username, name, group and subgroup by 'info' callback query message.

        :param query: Callback query message
        :type query: :obj:`types.CallbackQuery`

        :param state: User state machine context
        :type state: :obj:`FSMContext`
        """
        data = await state.get_data()
        await query.message.answer(MainHandlersChain.get_info(data))

    @staticmethod
    def get_info(user_data) -> str:
        """
        Gets to user information: username, name, group and subgroup from spreadsheet storage.

        :param user_data: User data
        :type user_data: :obj:`dict[Any]`

        :return: Returns information about user.
        :rtype: :obj:`str`
        """
        auth_data = user_data.get("auth")

        if user_data["type"] == "student":
            name = auth_data.get("name")
            group = auth_data.get("group")
            subgroup = auth_data.get("subgroup")

            return f"Информация о Вас:\nФИО: {name}\nГруппа: {group}\nПодгруппа: {subgroup}\n"
        elif user_data["type"] == "teacher":
            name = auth_data.get("ФИО")

            return f"Информация о Вас:\nФИО: {name}\n"

    @staticmethod
    @Registrar.message_handler(commands=["set_grade"], state="*")
    async def set_grade_start(message: types.Message, state: FSMContext):
        try:
            user_data = await state.get_data()
            if user_data.get("type") != "teacher":
                await message.answer("Эта операция доступна только преподавателям.")
                return

            await message.answer("Введите ФИО студента:")
            await state.set_state(MainStates.SELECT_STUDENT_FOR_GRADE)
        except Exception as e:
            MainHandlersChain._logger.error(f"Failed to initiate grade setting: {e}")
            await message.answer("Произошла ошибка. Попробуйте позже.")

    @staticmethod
    @Registrar.callback_query_handler(text="set_grade")
    async def set_grade_start_callback(query: types.CallbackQuery, state: FSMContext):
        try:
            user_data = await state.get_data()
            if user_data.get("type") != "teacher":
                await query.message.answer("Эта операция доступна только преподавателям.")
                return

            await query.message.answer("Введите ФИО студента:")
            await state.set_state(MainStates.SELECT_STUDENT_FOR_GRADE)
        except Exception as e:
            MainHandlersChain._logger.error(f"Failed to initiate grade setting from button: {e}")
            await query.message.answer("Произошла ошибка. Попробуйте позже.")

    @staticmethod
    @Registrar.message_handler(state=MainStates.SELECT_STUDENT_FOR_GRADE)
    async def set_lab_grade(message: types.Message, state: FSMContext):
        try:
            student_name = message.text.strip()

            works_spreadsheet_handler = WorksSpreadsheetHandler(
                spreadsheet_id=MainHandlersChain.work_spreadsheet_id,
                file_name=MainHandlersChain.path_to_work_token,
            )

            student_found = works_spreadsheet_handler.student_exists_by_name(student_name)
            if not student_found:
                await message.answer("Студент с таким ФИО не найден. Убедитесь, что вы ввели данные правильно.")
                return

            await state.update_data(student_name=student_name)
            await message.answer("Введите оценку за лабораторную работу (0-10):")
            await state.set_state(MainStates.SET_LAB_GRADE)
        except Exception as e:
            MainHandlersChain._logger.error(f"Failed to process student name: {e}")
            await message.answer("Произошла ошибка. Попробуйте позже.")
            await state.finish()

    @staticmethod
    @Registrar.message_handler(state=MainStates.SET_LAB_GRADE)
    async def save_lab_grade(message: types.Message, state: FSMContext):
        try:
            grade = message.text.strip()
            if not grade.isdigit() or not (0 <= int(grade) <= 10):
                await message.answer("Оценка должна быть числом от 0 до 10.")
                return

            grade = int(grade)
            data = await state.get_data()
            student_name = data.get("student_name")

            works_spreadsheet_handler = WorksSpreadsheetHandler(
                spreadsheet_id=MainHandlersChain.work_spreadsheet_id,
                file_name=MainHandlersChain.path_to_work_token,
            )

            success = works_spreadsheet_handler.update_lab_grade_by_name(student_name, grade)
            if success:
                await message.answer(f"Оценка {grade} успешно выставлена студенту {student_name}.")
            else:
                await message.answer(f"Не удалось выставить оценку студенту {student_name}. Проверьте данные.")
        except Exception as e:
            MainHandlersChain._logger.error(f"Failed to save lab grade: {e}")
            await message.answer("Произошла ошибка. Попробуйте позже.")
        finally:
            await state.finish()



