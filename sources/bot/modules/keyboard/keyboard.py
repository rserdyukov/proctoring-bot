from typing import List, Dict

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class KeyboardBuilder:
    @staticmethod
    def get_inline_keyboard_markup(buttons: List[Dict[str, str]]) -> InlineKeyboardMarkup:
        keyboards = []
        keyboard_group = []
        for group in buttons:
            for key in group:
                keyboard_group.append(InlineKeyboardButton(text=key, callback_data=str(group.get(key))))
            keyboards.append(keyboard_group)
            keyboard_group = []

        return InlineKeyboardMarkup(inline_keyboard=keyboards)
