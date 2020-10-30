import telegram
from telegram.utils.helpers import escape_markdown

from tgbot.models import User

def admin(update, context):
    """ Show help info about all secret admins commands """
    u = User.get_user(update, context)
    if not u.is_admin:
        return

    return update.message.reply_text("You will see secret admin commands when they will be added by devs")
    