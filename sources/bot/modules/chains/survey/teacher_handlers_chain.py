from typing import List

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from bot.loggers import LogInstaller
from bot.modules.chains.survey.menu_handlers_chain import GeneralSurveyStates
from bot.modules.handlers_chain import HandlersChain
from bot.modules.handlers_registrar import HandlersRegistrar as Registrar
from bot.modules.keyboard.keyboard import KeyboardBuilder


class SurveyTeacherStates(StatesGroup):
    starting_survey = State()


class SurveyTeacherKeyboardBuilder:
    @staticmethod
    def get_start_survey_keyboard(self):
        return KeyboardBuilder(
            [
                {
                    "Отправить": "send_survey",
                    "Вернуться": "cancel_survey"
                }
            ]
        )


class SurveyTeacherHandlersChain(HandlersChain):
    _logger = LogInstaller.get_default_logger(__name__, LogInstaller.DEBUG)

    @staticmethod
    @Registrar.callback_handler(text="start_survey", state=GeneralSurveyStates.teacher_survey)
    async def start_survey_handler(query: types.CallbackQuery, state: FSMContext):
        await SurveyTeacherStates.starting_survey.set()
        await Registrar.bot.send_message(query.message.chat.id, text=SurveyTeacherHandlersChain.get_survey())
        await query.message.edit_text("Отправить опрос студентам?")

    @staticmethod
    @Registrar.callback_handler(text="send_survey", state=SurveyTeacherStates.starting_survey)
    async def send_survey_handler(query: types.CallbackQuery, state: FSMContext):
        await query.message.edit_text("Опрос отправлен")
        await state.reset_state()

    @staticmethod
    @Registrar.callback_handler(text="cancel_survey", state=SurveyTeacherStates.starting_survey)
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
