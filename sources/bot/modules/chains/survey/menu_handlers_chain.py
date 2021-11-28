from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from bot.loggers import LogInstaller
from bot.modules.chains.main.main_handlers_chain import MainHandlersChain
from bot.modules.handlers_chain import HandlersChain
from bot.modules.handlers_registrar import HandlersRegistrar as Registrar
from bot.modules.keyboard.keyboard import KeyboardBuilder


class GeneralSurveyStates(StatesGroup):
    pass


class MenuKeyboardBuilder:
    @staticmethod
    def get_student_keyboard():
        return KeyboardBuilder.get_inline_keyboard_markup(
            [
                {
                    "Посмотреть результаты": "view_results"
                }
            ]
        )

    @staticmethod
    def get_teacher_keyboard():
        return KeyboardBuilder.get_inline_keyboard_markup(
            [
                {
                    "Запустить опрос": "start_survey",
                    "Проверитть вопросы": "check_survey"
                }
            ]
        )


class MenuHandlersChain(HandlersChain):
    _logger = LogInstaller.get_default_logger(__name__, LogInstaller.DEBUG)

    @staticmethod
    @Registrar.message_handler(commands=["survey"])
    async def show_menu_handler(message: types.Message, state: FSMContext):
        current_state = await state.get_state()
        data = await state.get_data()
        if data["type"] == "student":

            await message.answer("Привет, студент!", reply_markup=MenuKeyboardBuilder.get_student_keyboard())
        elif data["type"] == "teacher":
            await message.answer("Привет, преподаватель!!", reply_markup=MenuKeyboardBuilder.get_teacher_keyboard())
        else:
            await message.answer("Что-то пошло не так :(")
        # MenuHandlersChain._logger.debug(f"Cancel auth conversation state {current_state}")
