from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from tgbot.handlers.secret_level.manage_data import SECRET_LEVEL_BUTTON
from tgbot.handlers.secret_level.static_text import github_button_text, secret_level_button_text


def make_keyboard_for_start_command():
    buttons = [[
        InlineKeyboardButton(github_button_text, url="https://github.com/ohld/django-telegram-bot"),
        InlineKeyboardButton(secret_level_button_text, callback_data=f'{SECRET_LEVEL_BUTTON}')
    ]]

    return InlineKeyboardMarkup(buttons)