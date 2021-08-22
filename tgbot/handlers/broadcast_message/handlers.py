import re

import telegram

from tgbot.handlers.broadcast_message.manage_data import CONFIRM_DECLINE_BROADCAST, CONFIRM_BROADCAST
from tgbot.handlers.broadcast_message.keyboard_utils import keyboard_confirm_decline_broadcasting
from tgbot.handlers.broadcast_message import static_text
from tgbot.handlers.broadcast_message.utils import send_message
from tgbot.models import User
from tgbot.tasks import broadcast_message
from tgbot.handlers.utils import extract_user_data_from_update


def broadcast_command_with_message(update, context):
    """ Type /broadcast <some_text>. Then check your message in Markdown format and broadcast to users."""
    u = User.get_user(update, context)
    user_id = extract_user_data_from_update(update)['user_id']

    if not u.is_admin:
        text = static_text.broadcast_no_access
        markup = None
    else:
        text = f"{update.message.text.replace(f'{static_text.broadcast_command} ', '')}"
        markup = keyboard_confirm_decline_broadcasting()

    try:
        send_message(
            user_id=user_id,
            text=text,
            parse_mode=telegram.ParseMode.MARKDOWN,
            reply_markup=markup
        )
    except telegram.error.BadRequest as e:
        place_where_mistake_begins = re.findall(r"offset (\d{1,})$", str(e))
        text_error = static_text.error_with_markdown
        if len(place_where_mistake_begins):
            text_error += f"{static_text.specify_word_with_error}'{text[int(place_where_mistake_begins[0]):].split(' ')[0]}'"
        send_message(
            text=text_error,
            user_id=user_id
        )


def broadcast_decision_handler(update, context):
    # callback_data: CONFIRM_DECLINE_BROADCAST variable from manage_data.py
    """ Entered /broadcast <some_text>.
        Shows text in Markdown style with two buttons:
        Confirm and Decline
    """
    broadcast_decision = update.callback_query.data[len(CONFIRM_DECLINE_BROADCAST):]
    entities_for_celery = update.callback_query.message.to_dict().get('entities')
    entities, text = update.callback_query.message.entities, update.callback_query.message.text

    if broadcast_decision == CONFIRM_BROADCAST:
        admin_text = f"{static_text.message_is_sent}"
        user_ids = list(User.objects.all().values_list('user_id', flat=True))
        broadcast_message.delay(user_ids=user_ids, message=text, entities=entities_for_celery)
    else:
        admin_text = text

    context.bot.edit_message_text(
        text=admin_text,
        chat_id=update.callback_query.message.chat_id,
        message_id=update.callback_query.message.message_id,
        entities=None if broadcast_decision == CONFIRM_BROADCAST else entities
    )
