from cProfile import label

import validators
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import (
    StatesGroup,
    State,
)
from sources.bot.storage.service.schedule_service import ScheduleService
from datetime import datetime

from ...keyboard.keyboard import KeyboardBuilder
from ....loggers import LogInstaller
from ...handlers_chain import HandlersChain
from ...handlers_registrar import HandlersRegistrar as Registrar


class WorkStates(StatesGroup):
    title = State()
    text = State()
    difficulty = State()


class WorkKeyboardsBuilder:
    """
    This class uses to process inline-buttons

    """
    @staticmethod
    def get_labs_keyboard(labs) -> InlineKeyboardMarkup:
        """
        Gets keyboard to show all lab works to private user chat.

        :return: Returns inline keyboard markup.
        :rtype: :obj:`InlineKeyboardMarkup`
        """
        buttons = []
        for index, lab in enumerate(labs):
            lab_name = lab.get("labname", "Без названия")
            buttons.append(
                InlineKeyboardButton(
                    text=lab_name,
                    callback_data=f"lab_{index}"
                )
            )
        return InlineKeyboardMarkup(inline_keyboard=[[button] for button in buttons])


class WorkHandlersChain(HandlersChain):
    _logger = LogInstaller.get_default_logger(__name__, LogInstaller.DEBUG)
    _schedule_service = ScheduleService()

    @staticmethod
    @Registrar.message_handler(commands=["getlab"])
    async def get_lab_handler(message: types.Message, state: FSMContext):
        """
        Asks user to get all lab works to user.

        :param message: User message data
        :type message: :obj:`types.Message`

        :param state: User state machine context
        :type state: :obj:`FSMContext`
        """
        data = await state.get_data()
        labs = data.get("labs", [])

        if not labs:
            await message.answer("Лабораторные работы не найдены")
            return

        response = WorkHandlersChain.format_lab_info(labs)
        keyboard = WorkKeyboardsBuilder.get_labs_keyboard(labs)
        await message.answer(response, reply_markup=keyboard)

    @staticmethod
    @Registrar.callback_query_handler(lambda c: c.data.startswith("lab_"))
    async def lab_detail_callback_handler(query: types.CallbackQuery, state: FSMContext):
        """
           Asks user to get concrete lab work.

           :param message: User message data
           :type message: :obj:`types.Message`

           :param state: User state machine context
           :type state: :obj:`FSMContext`
           """
        index_str = query.data.split("_")[1]
        try:
            lab_index = int(index_str)
        except ValueError:
            await query.message.answer("Произошла ошибка при обработке данных.")
            await query.answer()
            return

        data = await state.get_data()
        labs = data.get("labs", [])

        if lab_index < 0 or lab_index >= len(labs):
            await query.message.answer("Лабораторная работа не найдена")
            await query.answer()
            return

        selected_lab = labs[lab_index]
        response = WorkHandlersChain.format_detailed_lab_info(selected_lab)

        await query.message.answer(response)
        await query.answer()

    @staticmethod
    def format_lab_info(labs) -> str:
        """
       Needs to show info of concrete labwork.

       :param message: User message data
       :type message: :obj:`types.Message`

       :param state: User state machine context
       :type state: :obj:`FSMContext`
       """
        if not labs:
            return "Информация о лабораторных работах отсутствует"

        response = "Лабораторные работы:\n\n"
        for lab in labs:
            lab_name = lab.get("labname", "Без названия")
            response += f"{lab_name}\n"

        return response.strip()

    @staticmethod
    def format_detailed_lab_info(lab) -> str:
        """
               Needs to show info of concrete labwork.

               :param message: User message data
               :type message: :obj:`types.Message`

               :param state: User state machine context
               :type state: :obj:`FSMContext`
               """
        lab_name = lab.get("labname", "Без названия")
        lab_content = lab.get("text", "Содержание отсутствует")
        lab_difficulty = lab.get("difficulty", "Содержание отсутствует")
        lab_deadline_date = lab.get("deadline_date", "Дедлайн отсутствует")

        response = f"Лабораторная работа: {lab_name}\n\n"
        response += f"Содержание:\n{lab_content}"
        response += f"Сложность:\n{lab_difficulty}"
        response += f"Дедлайн:\n{lab_deadline_date}"

        return response

    @staticmethod
    @Registrar.message_handler(commands=["addlab"])
    async def lab_start_handler(message: types.Message, state: FSMContext):
        """
               Asks teacher to upload new lab work.

               :param message: User message data
               :type message: :obj:`types.Message`

               :param state: User state machine context
               :type state: :obj:`FSMContext`
               """
        data = await state.get_data()
        await WorkStates.title.set()
        await message.answer("Отправьте название лабораторной работы.")


    @staticmethod
    @Registrar.callback_query_handler(text="addlab")
    async def lab_start_handler(query: types.CallbackQuery):
        """
                       Asks teacher to set title of the lab work.

                       :param message: User message data
                       :type message: :obj:`types.Message`

                       :param state: User state machine context
                       :type state: :obj:`FSMContext`
                       """
        WorkHandlersChain._logger.debug(f"Start lab conversation state")
        await WorkStates.title.set()
        await Registrar.bot.send_message(query.from_user.id, "Отправьте название лабораторной работы.")

    @staticmethod
    @Registrar.message_handler(lambda message: len(message.text.split(" "))!= 3, state=WorkStates.title)
    async def wrong_title_handler(message: types.Message):
        """
                       Notify user about wrong title of the lab work.

                       :param message: User message data
                       :type message: :obj:`types.Message`

                       :param state: User state machine context
                       :type state: :obj:`FSMContext`
                       """
        return await message.answer("Неправильное название для лабораторной работы.")

    @staticmethod
    @Registrar.message_handler(lambda message: len(message.text.split(" ")) == 3, state=WorkStates.title)
    async def process_title_handler(message: types.Message, state: FSMContext):
        """
                       Asks teacher to upload title of the lab work.

                       :param message: User message data
                       :type message: :obj:`types.Message`

                       :param state: User state machine context
                       :type state: :obj:`FSMContext`
                       """
        await WorkStates.next()
        await state.update_data(labs={"labname": message.text})
        await message.answer("Введите содержание лабораторной работы.")

    @staticmethod
    @Registrar.message_handler(state=WorkStates.text)
    async def process_text_handler(message: types.Message, state: FSMContext):
        """
                       Asks teacher to set lab difficulty of the lab work.

                       :param message: User message data
                       :type message: :obj:`types.Message`

                       :param state: User state machine context
                       :type state: :obj:`FSMContext`
                       """
        await WorkStates.next()
        data = await state.get_data()
        lab_data = data["labs"]
        lab_data["text"] = message.text
        await state.update_data(labs=lab_data)
        await message.answer("Введите сложность лабораторной работы.")

    @staticmethod
    @Registrar.message_handler(state=WorkStates.difficulty)
    async def process_difficulty_handler(message: types.Message, state: FSMContext):
        """
                       Shows user info about successfull adding of the new lab work.

                       :param message: User message data
                       :type message: :obj:`types.Message`

                       :param state: User state machine context
                       :type state: :obj:`FSMContext`
                       """
        await WorkStates.next()
        data = await state.get_data()
        lab_data = data["labs"]
        lab_data["difficulty"] = message.text
        await state.update_data(labs=lab_data)

        await message.answer(f"Лабораторная работа успешно добавлена.")
        username = message.from_user.username
        await state.update_data(username=username)

    @staticmethod
    @Registrar.message_handler(commands=["setdl"])
    async def set_deadlines(message: types.Message, state: FSMContext):
        """
                       Sets a deadline taking into account the complexity and dates of classes

                       :param message: User message data
                       :type message: :obj:`types.Message`

                       :param state: User state machine context
                       :type state: :obj:`FSMContext`
                       """
        data = await state.get_data()
        labs = data.get("labs", [])
        if not labs:
            await message.answer("Лабораторные работы не найдены")
            return

        difficulties = []
        for lab in labs:
            print(f'!!!!!!!{lab}')
            difficulties.append(int(lab["difficulty"]))

        deadlines = WorkHandlersChain._schedule_service.get_deadlines(difficulties)
        lessons_per_lab = WorkHandlersChain._schedule_service.distribute_lessons(deadlines)
        for lab, deadline in zip(labs, deadlines):
            lab["deadline_date"] = deadline.strftime("%d-%m-%Y")

        for lab, lesson_count in zip(labs, lessons_per_lab):
            lab["lab_lesson_count"] = lesson_count

        # Обновляем весь список лабораторных работ в состоянии
        await state.update_data(labs=labs)

        # Отправляем подтверждение
        await message.answer("Даты дедлайнов успешно обновлены!")
