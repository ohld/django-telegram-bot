"""
    Celery tasks. Some of them will be launched periodically from admin panel via django-celery-beat
"""

import time

from dtb.celery import app
from celery.utils.log import get_task_logger
from tgbot.handlers.utils import send_message
from tgbot.models import (
    Arcgis
)

logger = get_task_logger(__name__)

@app.task(ignore_result=True)
def broadcast_message(user_ids, message, entities=None, sleep_between=0.2, parse_mode=None) :
    logger.info(f"Going to send message: '{message}' to {len(user_ids)} users")

    for user_id in user_ids:
        try:
            send_message(user_id=user_id, text=message,  entities=entities, parse_mode=parse_mode)
            logger.info(f"Broadcast message was sent to {user_id}")
        except Exception as e:
            logger.error(f"Failed to send message to {user_id}, reason: {e}" )
        time.sleep(max(sleep_between, 0.1))

    logger.info("Broadcast finished!")


@app.task(ignore_result=True)
def save_data_from_arcgis(latitude, longitude, location_id):
    Arcgis.from_json(Arcgis.reverse_geocode(latitude, longitude), location_id=location_id)