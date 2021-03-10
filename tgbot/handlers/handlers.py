import datetime
import telegram
from telegram.messageentity import MessageEntity

from tgbot.handlers.manage_data import CONFIRM_DECLINE_BROADCAST, CONFIRM_BROADCAST
from tgbot.handlers.static_text import unlock_secret_room, broadcast_header, message_is_sent, \
    declined_message_broadcasting, broadcast_command
from tgbot.handlers.utils import handler_logging
from tgbot.models import User
from tgbot.tasks import broadcast_message
from tgbot.utils import extract_user_data_from_update
from django.utils import timezone


@handler_logging()
def secret_level(update, context):
    user_id = extract_user_data_from_update(update)['user_id']
    text = unlock_secret_room.format(
        user_count=User.objects.count(),
        active_24=User.objects.filter(updated_at__gte=timezone.now() - datetime.timedelta(hours=24)).count()
    )

    context.bot.edit_message_text(
        text=text,
        chat_id=user_id,
        message_id=update.callback_query.message.message_id,
        parse_mode=telegram.ParseMode.MARKDOWN
    )


def broadcast_decision_handler(update, context):
    broadcast_decision = update.callback_query.data[len(CONFIRM_DECLINE_BROADCAST):]
    print(update)
    # entities = update.callback_query.message.to_dict().get('entities')
    entities = update.callback_query.message.entities
    print("entities =", entities)

    text = update.callback_query.message.text#.replace(broadcast_header, "")
    if broadcast_decision == CONFIRM_BROADCAST:
        admin_text = f"{message_is_sent}"
        user_ids = list(User.objects.all().values_list('user_id', flat=True))
        print("user_ids = ", user_ids)
        context.bot.send_message(text=text,
                                 chat_id=350490234,
                                 # parse_mode=telegram.ParseMode.MARKDOWN,
                                 entities=entities)
        # broadcast_message.delay(user_ids=user_ids, message=text,
        #                         entities=entities)
    else:
        admin_text = f"{broadcast_command} {text}"


    context.bot.edit_message_text(
        text=admin_text,
        chat_id=update.callback_query.message.chat_id,
        message_id=update.callback_query.message.message_id,
        entities=entities
        # parse_mode=telegram.ParseMode.MARKDOWN,
    )