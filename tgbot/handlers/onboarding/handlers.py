import tgbot.handlers.onboarding.static_text
from tgbot.models import User
from tgbot.handlers.onboarding.keyboard_utils import make_keyboard_for_start_command


def command_start(update, context):
    u, created = User.get_user_and_created(update, context)

    if created:
        text = tgbot.handlers.onboarding.static_text.start_created.format(first_name=u.first_name)
    else:
        text = tgbot.handlers.onboarding.static_text.start_not_created.format(first_name=u.first_name)

    update.message.reply_text(text=text,
                              reply_markup=make_keyboard_for_start_command())