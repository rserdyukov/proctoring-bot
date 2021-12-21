"""
Keyboard builder implementation module.
"""
from typing import List, Dict

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class KeyboardBuilder:
    """
    Keyboard builder class implementation.
    """

    @staticmethod
    def get_inline_keyboard_markup(buttons: List[Dict[str, str]]) -> InlineKeyboardMarkup:
        """
        Keyboard builder class implementation.

        :param buttons: List of buttons names and callback query messages dictionaries
        :type buttons: :obj:`list[Dict[str, str]]`

        :return: Returns inline keyboard markup instance.
        :rtype: :obj:`InlineKeyboardMarkup`
        """
        keyboards = []
        keyboard_group = []
        for group in buttons:
            for key in group:
                keyboard_group.append(InlineKeyboardButton(text=key, callback_data=str(group.get(key))))
            keyboards.append(keyboard_group)
            keyboard_group = []

        return InlineKeyboardMarkup(inline_keyboard=keyboards)
