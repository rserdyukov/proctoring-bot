from typing import List

import validators
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup

from ....loggers import LogInstaller
from ....modules.handlers_chain import HandlersChain
from ....modules.handlers_registrar import HandlersRegistrar as Registrar
from ....modules.keyboard.keyboard import KeyboardBuilder


class SurveyTeacherStates(StatesGroup):
    waiting_for_link = State()
    starting_survey = State()


class SurveyTeacherKeyboardBuilder:
    @staticmethod
    def get_cancel_survey_keyboard():
        return KeyboardBuilder.get_inline_keyboard_markup(
            [
                {
                    "Вернуться": "cancel_survey",
                }
            ]
        )

    @staticmethod
    def get_student_start_keyboard(survey_sheet_name: str) -> InlineKeyboardMarkup:
        return KeyboardBuilder.get_inline_keyboard_markup(
            [
                {
                    "Начать тест": f"start;{survey_sheet_name};0",
                }
            ]
        )

    @staticmethod
    def get_answers_keyboard(question: dict, question_number: int, survey_sheet_name: str):
        answers = []
        keys = list(question.keys())
        next_question_number = question_number + 1
        for answer in keys:
            if answer.startswith("ответ"):
                answers.append({f"{question[answer]}": f"question;{survey_sheet_name};{next_question_number};{answer}"})

        return KeyboardBuilder.get_inline_keyboard_markup(answers)

    @staticmethod
    def get_start_survey_keyboard():
        return KeyboardBuilder.get_inline_keyboard_markup(
            [
                {
                    "Отправить": "send_survey",
                    "Вернуться": "cancel_survey",
                }
            ]
        )


class SurveyTeacherHandlersChain(HandlersChain):
    _logger = LogInstaller.get_default_logger(__name__, LogInstaller.DEBUG)

    @staticmethod
    @Registrar.message_handler(commands=["survey"])  # needs to change to callback after main menu button pressed
    async def survey_link_get_handler(message: types.Message, state: FSMContext):
        data = await state.get_data()
        if data["type"] == "teacher":
            await SurveyTeacherStates.waiting_for_link.set()
            await message.answer("Отправьте ссылку на таблицу с тестом",
                                 reply_markup=SurveyTeacherKeyboardBuilder.get_cancel_survey_keyboard())

    @staticmethod
    @Registrar.message_handler(state=SurveyTeacherStates.waiting_for_link)
    async def link_message_handler(message: types.Message, state: FSMContext):
        if validators.url(str(message.text)):
            await SurveyTeacherStates.starting_survey.set()

            await state.update_data(tests={"test_link": message.text})
            data = await state.get_data()
            tests_data = data.get("tests")
            test = tests_data.get("test")

            question_number = 0
            for question in test:
                answers_kb = SurveyTeacherKeyboardBuilder.get_answers_keyboard(question, question_number,
                                                                               tests_data["test_name"])
                question_number += 1
                await message.answer(f"{question['Вопрос']}",
                                     reply_markup=answers_kb)
            await message.answer(f"Выведено {question_number} вопросов\n"
                                 f"Отправить студентам?",
                                 reply_markup=SurveyTeacherKeyboardBuilder.get_start_survey_keyboard())
        else:
            await message.answer("Неправильная ссылка, попробуйте еще раз",
                                 reply_markup=SurveyTeacherKeyboardBuilder.get_cancel_survey_keyboard())

    @staticmethod
    @Registrar.callback_query_handler(text="send_survey", state=SurveyTeacherStates.starting_survey)
    async def start_survey_handler(query: types.CallbackQuery, state: FSMContext):
        data = await state.get_data()
        students = data.get("students")
        tests = data.get("tests")
        test_name = tests.get("test_name")
        student_count = 0
        for student in students:
            await query.message.bot.send_message(text="Доступен новый тест.\n"
                                                      "Чтобы приступить, нажмите кнопку ниже",
                                                 reply_markup=SurveyTeacherKeyboardBuilder.
                                                 get_student_start_keyboard(test_name),
                                                 chat_id=student)
            student_count += 1
        await query.answer()
        await SurveyTeacherStates.next()
        await query.message.edit_text(f"Опрос отправлен {student_count} студентам")

    @staticmethod
    @Registrar.callback_query_handler(text="cancel_survey", state="*")
    async def cancel_survey_handler(query: types.CallbackQuery, state: FSMContext):
        await query.message.edit_text("Отправка опроса отменена")
        await state.reset_state()
