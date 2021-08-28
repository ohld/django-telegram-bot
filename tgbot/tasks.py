"""
    Celery tasks. Some of them will be launched periodically from admin panel via django-celery-beat
"""

import time

from dtb.celery import app
from celery.utils.log import get_task_logger
from tgbot.handlers.broadcast_message.utils import send_message

logger = get_task_logger(__name__)


@app.task(ignore_result=True)
def broadcast_message(user_ids, message, entities=None, sleep_between=0.4, parse_mode=None):
    """ It's used to broadcast message to big amount of users """
    logger.info(f"Going to send message: '{message}' to {len(user_ids)} users")

    for user_id in user_ids:
        try:
            send_message(user_id=user_id, text=message,  entities=entities, parse_mode=parse_mode)
            logger.info(f"Broadcast message was sent to {user_id}")
        except Exception as e:
            logger.error(f"Failed to send message to {user_id}, reason: {e}")
        time.sleep(max(sleep_between, 0.1))

    logger.info("Broadcast finished!")


