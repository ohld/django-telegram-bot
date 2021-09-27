from typing import Union, Optional, Dict

import telegram
from telegram import MessageEntity

from dtb.settings import TELEGRAM_TOKEN
from tgbot.models import User


def _send_message(
    user_id: Union[str, int],
    text: str,
    parse_mode: Optional[str] = None,
    reply_markup: Optional[Dict] = None,
    reply_to_message_id: Optional[int] = None,
    disable_web_page_preview: Optional[bool] = None,
    entities: Optional[Dict] = None,
    tg_token: str = TELEGRAM_TOKEN,
) -> bool:
    bot = telegram.Bot(tg_token)
    try:
        if entities:
            entities = [
                MessageEntity(
                    type=entity['type'],
                    offset=entity['offset'],
                    length=entity['length']
                )
                for entity in entities
            ]

        m = bot.send_message(
            chat_id=user_id,
            text=text,
            parse_mode=parse_mode,
            reply_markup=reply_markup,
            reply_to_message_id=reply_to_message_id,
            disable_web_page_preview=disable_web_page_preview,
            entities=entities,
        )
    except telegram.error.Unauthorized:
        print(f"Can't send message to {user_id}. Reason: Bot was stopped.")
        User.objects.filter(user_id=user_id).update(is_blocked_bot=True)
        success = False
    except Exception as e:
        print(f"Can't send message to {user_id}. Reason: {e}")
        success = False
    else:
        success = True
        User.objects.filter(user_id=user_id).update(is_blocked_bot=False)
    return success
