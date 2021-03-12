import telegram
import datetime
import re

from tgbot.handlers.keyboard_utils import make_keyboard_for_start_command, keyboard_confirm_decline_broadcasting
from tgbot.handlers.static_text import start_created, start_not_created, broadcast_no_access, broadcast_header, \
    broadcast_command, error_with_markdown, specify_word_with_error
from tgbot.handlers.utils import handler_logging
from tgbot.models import User
from django.utils import timezone


# @send_typing_action
from tgbot.utils import extract_user_data_from_update


@handler_logging()
def start(update, context):
    u, created = User.get_user_and_created(update, context)

    if created:
        text = start_created.format(first_name=u.first_name)
    else:
        text = start_not_created.format(first_name=u.first_name)


    update.message.reply_text(text=text,
                              reply_markup=make_keyboard_for_start_command())


def stats(update, context):
    """ Show help info about all secret admins commands """
    u = User.get_user(update, context)
    if not u.is_admin:
        return

    text = f"""
*Users*: {User.objects.count()}
*24h active*: {User.objects.filter(updated_at__gte=timezone.now() - datetime.timedelta(hours=24)).count()}
    """

    return update.message.reply_text(
        text, 
        parse_mode=telegram.ParseMode.MARKDOWN,
        disable_web_page_preview=True,
    )


def broadcast_command_with_message(update, context):
    u = User.get_user(update, context)
    user_id = extract_user_data_from_update(update)['user_id']

    if not u.is_admin:
        text = broadcast_no_access
        markup = None

    else:
        text = f"{update.message.text.replace(f'{broadcast_command} ', '')}"
        markup = keyboard_confirm_decline_broadcasting()

    try:
        context.bot.send_message(
            text=text,
            chat_id=user_id,
            parse_mode=telegram.ParseMode.MARKDOWN,
            reply_markup=markup
        )
    except telegram.error.BadRequest as e:
        place_where_mistake_begins = re.findall(r"offset (\d{1,})$", str(e))
        text_error = error_with_markdown
        if len(place_where_mistake_begins):
            text_error += f"{specify_word_with_error}'{text[int(place_where_mistake_begins[0]):].split(' ')[0]}'"
        context.bot.send_message(
            text=text_error,
            chat_id=user_id
        )