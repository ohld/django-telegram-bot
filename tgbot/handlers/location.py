import telegram

from tgbot.handlers.static_text import share_location, thanks_for_location
from tgbot.models import User, Location


def ask_for_location(update, context):
    u = User.get_user(update, context)

    context.bot.send_message(
        chat_id=u.user_id, text=share_location,
        reply_markup=telegram.ReplyKeyboardMarkup([
            [telegram.KeyboardButton(text="Send 🌏🌎🌍", request_location=True)]
        ], resize_keyboard=True), #'False' will make this button appear on half screen (become very large). Likely,
        # it will increase click conversion but may decrease UX quality.
    )


def location_handler(update, context):
    u = User.get_user(update, context)
    lat, lon = update.message.location.latitude, update.message.location.longitude
    l = Location.objects.create(user=u, latitude=lat, longitude=lon)

    update.message.reply_text(
        thanks_for_location,
        reply_markup=telegram.ReplyKeyboardRemove(),
    )    
