import time
import telegram

from tgbot.models import User

# @send_typing_action
def start(update, context):
    u, created = User.get_user_and_created(update, context)

    if created:
        return update.message.reply_text(f"sup {u.first_name}!")

    return update.message.reply_text(f"welcome back {u.first_name}!")