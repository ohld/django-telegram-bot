import datetime
import telegram
import os

from tgbot.handlers.utils import handler_logging
from tgbot.models import User
from tgbot.utils import extract_user_data_from_update

bot = telegram.Bot(os.getenv("TELEGRAM_TOKEN"))

@handler_logging()
def secret_level(update, context):
    user_id = extract_user_data_from_update(update)['user_id']
    text = f"Congratulations! You've opened a secret room👁‍🗨. There is some information for you:\n" \
           f"*Users*: {User.objects.count()}\n" \
           f"*24h active*: {User.objects.filter(updated_at__gte=datetime.datetime.now() - datetime.timedelta(hours=24)).count()}"

    bot.edit_message_text(text=text,
                          chat_id=user_id,
                          message_id=update.callback_query.message.message_id,
                          parse_mode=telegram.ParseMode.MARKDOWN)
