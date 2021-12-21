from typing import List

from urlvalidator import URLValidator, ValidationError
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from bot.loggers import LogInstaller
from bot.modules.handlers_chain import HandlersChain
from bot.modules.handlers_registrar import HandlersRegistrar as Registrar
from bot.storage.spreadsheet.tests.tests_spreadsheet_handler import TestsSpreadsheetHandler
from bot.modules.keyboard.keyboard import KeyboardBuilder


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
    @Registrar.message_handler(commands=["survey"])
    async def survey_link_get_handler(message: types.Message):
        await SurveyTeacherStates.waiting_for_link.set()
        await message.answer("Отправьте ссылку на таблицу с тестом",
                             reply_markup=SurveyTeacherKeyboardBuilder.get_cancel_survey_keyboard())

    @staticmethod
    @Registrar.message_handler(state=SurveyTeacherStates.waiting_for_link)
    async def link_message_handler(message: types.Message):
        validate = URLValidator()
        try:
            validate(message.text)
            await SurveyTeacherStates.starting_survey.set()
            await Registrar.bot.send_message(message.chat.id, text="Здесь будет тест")
            await message.answer("Отправить опрос студентам?",
                                 reply_markup=SurveyTeacherKeyboardBuilder.get_start_survey_keyboard())
        except ValidationError as exception:
            await message.answer("Неправильная ссылка, попробуйте еще раз",
                                 reply_markup=SurveyTeacherKeyboardBuilder.get_cancel_survey_keyboard())

    @staticmethod
    @Registrar.callback_query_handler(text="start_survey", state=SurveyTeacherStates.starting_survey)
    async def start_survey_handler(query: types.CallbackQuery, state: FSMContext):
        await Registrar.bot.send_message(query.message.chat.id, text="Здесь будет тест")
        await query.message.edit_text("Опрос отправлен n студентам",
                                      reply_markup=SurveyTeacherKeyboardBuilder.get_cancel_survey_keyboard())

    @staticmethod
    @Registrar.callback_query_handler(text="cancel_survey", state="*")
    async def cancel_survey_handler(query: types.CallbackQuery, state: FSMContext):
        await query.message.edit_text("Отправка опроса отменена")
        await state.reset_state()

    @staticmethod
    def get_survey() -> List[dict]:
        return [
            {
                "Вопрос1": "содержание вопроса",
                "ответ1": "содержание ответа",
                "ответ2": "содержание ответа",
                "ответ3": "содержание ответа",
                "ответ4": "содержание ответа",
                "правильный": "ответ1"
            }
        ]
