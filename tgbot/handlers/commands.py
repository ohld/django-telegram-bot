import time
import telegram

from tgbot.handlers.utils import handler_logging
from tgbot.models import User

# @send_typing_action
@handler_logging
def start(update, context):
    u, created = User.get_user_and_created(update, context)

    if created:
        return update.message.reply_text(f"sup {u.first_name}!")

    return update.message.reply_text(f"welcome back, {u.first_name}!")


def stats(update, context):
    """ Show help info about all secret admins commands """
    u = User.get_user(update, context)
    if not u.is_admin:
        return

    text = f"""
*Users*: {User.objects.count()}
*24h active*: {User.objects.filter(updated_at__gte=now() - datetime.timedelta(hours=24)).count()}
    """

    return update.message.reply_text(
        text, 
        parse_mode=telegram.ParseMode.MARKDOWN,
        disable_web_page_preview=True,
    )
    