from telegram import InlineKeyboardButton as inlinebutton,\
    InlineKeyboardMarkup as inlinemarkup

from tgbot.handlers.manage_data import SECRET_LEVEL_BUTTON


def make_keyboard_for_start_command():
    buttons = [[
        inlinebutton("GitHub", url="https://github.com/ohld/django-telegram-bot"),
        inlinebutton("Secret level🗝", callback_data=f'{SECRET_LEVEL_BUTTON}')
    ]]

    return inlinemarkup(buttons)