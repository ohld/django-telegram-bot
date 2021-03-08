"""
    Celery tasks. Some of them will be launched periodically from admin panel via django-celery-beat
"""

import time
import telegram

from dtb.celery import app
from celery.utils.log import get_task_logger

from dtb.settings import TELEGRAM_TOKEN
from tgbot.models import (
    User, Arcgis
)

logger = get_task_logger(__name__)

@app.task(ignore_result=True)
def broadcast_message(user_ids, message, sleep_between=0.2):
    logger.info(f"Going to send message: '{message}' to {len(user_ids)} users")

    for user_id in user_ids:
        try:
            u = User.objects.get(user_id=user_id)
            u.send_message(message=message, parse_mode=telegram.ParseMode.MARKDOWN)
            logger.info(f"Broadcast message was sent to {u}")
        except Exception as e:
            logger.error(f"Failed to send message to {u}, reason: {e}" )
        time.sleep(max(sleep_between, 0.1))

    logger.info("Broadcast finished!")


@app.task(ignore_result=True)
def send_payment_confirmation(user_id):
    u = User.objects.filter(user_id=user_id).first()

    bot = telegram.Bot(TELEGRAM_TOKEN)
    bot.send_animation(
        chat_id=user_id,
        animation="",  # TODO: add file_id of sexy animation
        caption=f"""
😱 Wow! Welcome to Private Party.

😘 Your purchase was successful.

💰 Now your balance is ${u.balance}!

Like it? Share @best_smm_panel_bot with friends 👇
        """,
        reply_markup=telegram.InlineKeyboardMarkup([
            [
                telegram.InlineKeyboardButton("Share Bot! 😛", url=f'https://t.me/share/url?url=t.me/best_smm_panel_bot&text=Try%20it%2C%20I%20wonder%20what%20you%20get%20%F0%9F%98%8F'),
            ],
        ]),
    )


@app.task(ignore_result=True)
def save_data_from_arcgis(latitude, longitude, location_id):
    Arcgis.from_json(Arcgis.reverse_geocode(latitude, longitude), location_id=location_id)