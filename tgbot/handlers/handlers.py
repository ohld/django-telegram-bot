import datetime
import telegram

from tgbot.handlers.static_text import unlock_secret_room
from tgbot.handlers.utils import handler_logging
from tgbot.models import User
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
