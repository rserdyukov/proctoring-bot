from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from ....loggers import LogInstaller
from ...handlers_chain import HandlersChain
from ...handlers_registrar import HandlersRegistrar as Registrar
from ....storage.spreadsheet.subjects.subject_spreadsheet_handler import SubjectSpreadsheetHandler


class SubjectStates(StatesGroup):
    waiting_for_subject_name = State()
    waiting_for_subject_description = State()
    waiting_for_subject_lookup = State()


class SubjectHandlersChain(HandlersChain):
    _logger = LogInstaller.get_default_logger(__name__, LogInstaller.DEBUG)

    @staticmethod
    @Registrar.message_handler(commands=["subject_description_add"], state="*")
    async def subject_start_message_handler(message: types.Message):
        SubjectHandlersChain._logger.debug("Start subject conversation state")
        await message.answer("Введите название дисциплины:")
        await SubjectStates.waiting_for_subject_name.set()

    @staticmethod
    @Registrar.callback_query_handler(text="subject_description_add")
    async def subject_start_callback_handler(query: types.CallbackQuery):
        SubjectHandlersChain._logger.debug("Start subject conversation state")
        await Registrar.bot.send_message(query.from_user.id, "Введите название дисциплины:")
        await SubjectStates.waiting_for_subject_name.set()

    @staticmethod
    @Registrar.message_handler(state=SubjectStates.waiting_for_subject_name)
    async def subject_name_handler(message: types.Message, state: FSMContext):
        subject_name = message.html_text.strip()  # Используем HTML-разметку

        if not subject_name:
            await message.answer("Название дисциплины не может быть пустым. Попробуйте еще раз:")
            return

        await state.update_data(subject_name=subject_name)
        await message.answer("Введите описание дисциплины:")
        await SubjectStates.waiting_for_subject_description.set()

    @staticmethod
    @Registrar.message_handler(state=SubjectStates.waiting_for_subject_description)
    async def subject_description_handler(message: types.Message, state: FSMContext):
        subject_description = message.html_text.strip()

        if not subject_description:
            await message.answer("Описание дисциплины не может быть пустым. Попробуйте еще раз:")
            return

        data = await state.get_data()
        subject_name = data.get('subject_name')

        await state.update_data(subject_description=subject_description)
        try:
            spreadsheet_handler = SubjectSpreadsheetHandler(
                spreadsheet_id="1R8PFRfrb8NRjyCQMZLExXvNEoA8_xvDTACvmdExO70U",
                file_name="sources/tokens/subjects_token.json"
            )
            spreadsheet_handler.add_subject(subject_name, subject_description)
            await message.answer("Название и описание дисциплины успешно сохранены в таблицу.")
        except Exception as e:
            SubjectHandlersChain._logger.error(f"Error adding subject: {e}")
            await message.answer("Произошла ошибка при сохранении данных. Попробуйте позже.")

        SubjectHandlersChain._logger.debug(
            f"Finite subject conversation state. Name: {subject_name}, Description: {subject_description}"
        )
        await state.finish()

    @staticmethod
    @Registrar.callback_query_handler(text="get_subject_description")
    async def subject_description_lookup_handler(query: types.CallbackQuery):
        SubjectHandlersChain._logger.debug("Start subject description lookup")
        await Registrar.bot.send_message(query.from_user.id, "Введите название дисциплины:")
        await SubjectStates.waiting_for_subject_lookup.set()

    @staticmethod
    @Registrar.message_handler(state=SubjectStates.waiting_for_subject_lookup)
    async def subject_lookup_handler(message: types.Message, state: FSMContext):
        subject_name = message.text.strip()

        if not subject_name:
            await message.answer("Название дисциплины не может быть пустым. Попробуйте ещё раз.")
            return

        try:
            spreadsheet_handler = SubjectSpreadsheetHandler(
                spreadsheet_id="1R8PFRfrb8NRjyCQMZLExXvNEoA8_xvDTACvmdExO70U",
                file_name="sources/tokens/subjects_token.json"
            )
            description = spreadsheet_handler.get_subject_description(subject_name)

            await message.answer(f"Информация о дисциплине \"{subject_name}\":\n{description}", parse_mode="HTML")
            SubjectHandlersChain._logger.debug(f"Found description for {subject_name}: {description}")
        except Exception as e:
            SubjectHandlersChain._logger.error(f"Error fetching description: {e}")
            await message.answer(f"Не удалось найти описание для дисциплины '{subject_name}'."
                                 f" Проверьте название и попробуйте снова.")
        finally:
            await state.finish()

