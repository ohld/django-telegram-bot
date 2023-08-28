from functools import wraps
from typing import Callable

from telegram import Update, ChatAction
from telegram.ext import CallbackContext

from users.models import User


def admin_only(reply_message: str = None):
    """
    Admin only decorator
    Used for handlers that only admins have access to

    @param reply_message: message to reply
    """

    def decorator(func: Callable):
        @wraps(func)
        def inner(update: Update, context: CallbackContext, *args, **kwargs):
            user = User.get_user(update, context)

            if not user.is_admin:
                if reply_message is not None and update.effective_message:
                    update.effective_message.reply_text(reply_message)
                return

            return func(update, context, *args, **kwargs)

        return inner

    return decorator


def send_typing_action(func: Callable):
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(update: Update, context: CallbackContext, *args, **kwargs):
        update.effective_chat.send_chat_action(ChatAction.TYPING)
        return func(update, context, *args, **kwargs)

    return command_func
