import time
import telegram
from telegram.utils.helpers import escape_markdown

from dtb.settings import TELEGRAM_TOKEN

from tgbot.models import User

bot = telegram.Bot(TELEGRAM_TOKEN)

CHAT_ID = 49820636  # ENTER CHAT ID for logs

def send_text(text):
    bot.send_message(
        chat_id=CHAT_ID,
        text=text,
        parse_mode=telegram.ParseMode.MARKDOWN,
    )