import telegram
from functools import wraps
from dtb.settings import ENABLE_DECORATOR_LOGGING
from django.utils import timezone
from tgbot.models import UserActionLog
from tgbot.utils import extract_user_data_from_update


def send_typing_action(func):
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=telegram.ChatAction.TYPING)
        return func(update, context,  *args, **kwargs)

    return command_func


def handler_logging(action_name=None):
    def decor(func):
        def handler(update, context, *args, **kwargs):
            user_id = extract_user_data_from_update(update)['user_id']
            action = f"{func.__module__}.{func.__name__}" if not action_name else action_name
            UserActionLog.objects.create(user_id=user_id, action=action, created_at=timezone.now())
            return func(update, context, *args, **kwargs)
        return handler if ENABLE_DECORATOR_LOGGING else func
    return decor

