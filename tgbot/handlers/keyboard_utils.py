from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from tgbot.handlers.manage_data import SECRET_LEVEL_BUTTON, CONFIRM_DECLINE_BROADCAST, CONFIRM_BROADCAST, \
    DECLINE_BROADCAST
from tgbot.handlers.static_text import github_button_text, secret_level_button_text, confirm_broadcast, \
    decline_broadcast


def make_keyboard_for_start_command():
    buttons = [[
        InlineKeyboardButton(github_button_text, url="https://github.com/ohld/django-telegram-bot"),
        InlineKeyboardButton(secret_level_button_text, callback_data=f'{SECRET_LEVEL_BUTTON}')
    ]]

    return InlineKeyboardMarkup(buttons)


def keyboard_confirm_decline_broadcasting():
    buttons = [[
        InlineKeyboardButton(confirm_broadcast, callback_data=f'{CONFIRM_DECLINE_BROADCAST}{CONFIRM_BROADCAST}'),
        InlineKeyboardButton(decline_broadcast, callback_data=f'{CONFIRM_DECLINE_BROADCAST}{DECLINE_BROADCAST}')
    ]]

    return InlineKeyboardMarkup(buttons)