import telegram
import datetime

from tgbot.handlers.keyboard_utils import make_keyboard_for_start_command
from tgbot.handlers.utils import handler_logging
from tgbot.models import User


# @send_typing_action
@handler_logging()
def start(update, context):
    u, created = User.get_user_and_created(update, context)

    if created:
        text = f"sup {u.first_name}!"
    else:
        text = f"welcome back, {u.first_name}!"


    update.message.reply_text(text=text,
                              reply_markup=make_keyboard_for_start_command())


def stats(update, context):
    """ Show help info about all secret admins commands """
    u = User.get_user(update, context)
    if not u.is_admin:
        return

    text = f"""
*Users*: {User.objects.count()}
*24h active*: {User.objects.filter(updated_at__gte=datetime.datetime.now() - datetime.timedelta(hours=24)).count()}
    """

    return update.message.reply_text(
        text, 
        parse_mode=telegram.ParseMode.MARKDOWN,
        disable_web_page_preview=True,
    )
    