"""
    Celery tasks. Some of them will be launched periodically from admin panel via django-celery-beat
"""

import time
import random
import telegram
import datetime

from telegram.error import BadRequest

from django.utils.timezone import now
from django.db.models import Count

from celery.decorators import task
from celery.utils.log import get_task_logger

from dtb.settings import TELEGRAM_TOKEN
from tgbot.models import (
    User,
)

logger = get_task_logger(__name__)

@task(ignore_result=True)
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