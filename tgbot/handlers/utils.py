import telegram
from functools import wraps
from dtb.settings import ENABLE_DECORATOR_LOGGING
from django.utils import timezone


def send_typing_action(func):
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=telegram.ChatAction.TYPING)
        return func(update, context,  *args, **kwargs)

    return command_func


def get_userid_from_update(update):
    if update.callback_query:
        user_id = update.callback_query.from_user.id
    elif update.inline_query:
        user_id = update.inline_query.from_user.id
    else:
        user_id = update.message.from_user.id

    return user_id


def handler_logging(func):
    def handler(update, context, *args, **kwargs):
        user_id = get_userid_from_update(update)
        print(f"user with id = {user_id} pressed {func.__name__} at {timezone.now()}")
        return func(update, context, *args, **kwargs)


    return handler if ENABLE_DECORATOR_LOGGING else func