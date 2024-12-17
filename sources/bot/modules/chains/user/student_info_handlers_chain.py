"""
Bot student info handlers chain implementation module.
"""

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ChatType, InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup

from ..survey.student_handlers_chain import StudentHandlersChain
from ...handlers_chain import HandlersChain
from ...handlers_registrar import HandlersRegistrar as Registrar
from ....loggers import LogInstaller


class UserInfoStates(StatesGroup):
    """
    Bot student info handlers chain states class implementation.
    """

    group = State()
    choice = State()


class StudentInfoKeyboardsBuilder:
    """
    Bot student info handlers chain keyboard builder class implementation.
    """

    @staticmethod
    def get_private_group_student_list_keyboard(group_students) -> InlineKeyboardMarkup:
        buttons = []
        for stud_id, stud_data in group_students.items():
            name = stud_data['name']
            stud_sub = stud_data['subgroup']
            buttons.append(
                InlineKeyboardButton(
                    text=f"{stud_sub} | {name}",
                    callback_data=f"student_{stud_id}"
                )

            )
        return InlineKeyboardMarkup(inline_keyboard=[[button] for button in buttons])


class StudentInfoHandlersChain(HandlersChain):
    """
    Bot student info handlers chain class implementation.
    """

    _logger = LogInstaller.get_default_logger(__name__, LogInstaller.DEBUG)

    @staticmethod
    @Registrar.message_handler(commands=['get_student_info'], chat_type=ChatType.PRIVATE)
    async def start_handler(message: types.Message):
        StudentInfoHandlersChain._logger.debug("Start user info conversation state")
        await UserInfoStates.group.set()

        await Registrar.bot.send_message(message.from_user.id, "Введите номер группы студента")

    @staticmethod
    @Registrar.callback_query_handler(text="get_student_info")
    async def start_handler(query: types.CallbackQuery):
        StudentInfoHandlersChain._logger.debug("Start user info conversation state")
        await UserInfoStates.group.set()

        await Registrar.bot.send_message(query.from_user.id, "Введите номер группы студента")

    @staticmethod
    @Registrar.message_handler(regexp=r"[0-9]{6}", state=UserInfoStates.group)
    async def process_group_handler(message: types.Message, state: FSMContext):
        await UserInfoStates.next()

        data = await state.get_data()
        group = message.text

        group_students = StudentInfoHandlersChain._get_group_students(group, data["students"])
        if group_students == {}:
            await message.answer("В этой группе нет студентов!")
            await UserInfoStates.next()
            return

        keyboard_markup = (StudentInfoKeyboardsBuilder
                           .get_private_group_student_list_keyboard(group_students))

        await message.answer(f"Студенты группы {group}\n(Подгруппа | Фио)", reply_markup=keyboard_markup)

    @staticmethod
    @Registrar.callback_query_handler(lambda c: c.data.startswith("student_"), state=UserInfoStates.choice)
    async def student_selected_handler(query: types.CallbackQuery, state: FSMContext):
        StudentHandlersChain._logger.debug("Finite user info conversation state")
        await UserInfoStates.next()

        stud_id = query.data.split("_")[1]
        data = await state.get_data()
        student_data = data["students"][stud_id]
        name = student_data['name']
        group = student_data['group']
        subgroup = student_data['subgroup']

        await query.message.answer(f"Информация о студенте:\nФИО: {name}\nГруппа: {group}\nПодгруппа: {subgroup}\n")
        await query.answer()

    @staticmethod
    def _get_group_students(group, students_data):
        result_students = {}
        for stud_id, stud_data in students_data.items():
            if stud_data['group'] == group:
                result_students[stud_id] = stud_data
        return result_students

