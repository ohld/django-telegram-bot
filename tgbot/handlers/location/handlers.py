import telegram

import tgbot.handlers.broadcast_message.utils
from tgbot.handlers.location.static_text import share_location, thanks_for_location
from tgbot.handlers.location.keyboard_utils import send_location_keyboard
from tgbot.models import User, Location


def ask_for_location(update, context):
    """ Entered /ask_location command"""
    u = User.get_user(update, context)

    tgbot.handlers.broadcast_message.utils.send_message(
        chat_id=u.user_id,
        text=share_location,
        reply_markup=send_location_keyboard()
    )


def location_handler(update, context):
    # receiving user's location
    u = User.get_user(update, context)
    lat, lon = update.message.location.latitude, update.message.location.longitude
    Location.objects.create(user=u, latitude=lat, longitude=lon)

    update.message.reply_text(
        thanks_for_location,
        reply_markup=telegram.ReplyKeyboardRemove(),
    )
