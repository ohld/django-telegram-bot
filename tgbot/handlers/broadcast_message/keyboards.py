from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from tgbot.handlers.broadcast_message.manage_data import CONFIRM_DECLINE_BROADCAST, CONFIRM_BROADCAST, DECLINE_BROADCAST
from tgbot.handlers.broadcast_message.static_text import confirm_broadcast, decline_broadcast


def keyboard_confirm_decline_broadcasting() -> InlineKeyboardMarkup:
    buttons = [[
        InlineKeyboardButton(confirm_broadcast, callback_data=f'{CONFIRM_DECLINE_BROADCAST}{CONFIRM_BROADCAST}'),
        InlineKeyboardButton(decline_broadcast, callback_data=f'{CONFIRM_DECLINE_BROADCAST}{DECLINE_BROADCAST}')
    ]]

    return InlineKeyboardMarkup(buttons)
