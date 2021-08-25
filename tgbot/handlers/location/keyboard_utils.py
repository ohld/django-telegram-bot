from telegram import ReplyKeyboardMarkup, KeyboardButton

from tgbot.handlers.location.static_text import SEND_LOCATION


def send_location_keyboard():
    # resize_keyboard=False will make this button appear on half screen (become very large).
    # Likely, it will increase click conversion but may decrease UX quality.
    return ReplyKeyboardMarkup(
        [[KeyboardButton(text=SEND_LOCATION, request_location=True)]],
        resize_keyboard=True
    ),
