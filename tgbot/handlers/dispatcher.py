# 
    Add handlers to dispatcher
#

import telegram
from telegram.ext import (
    Updater, Dispatcher, Filters,
    CommandHandler, MessageHandler,
    InlineQueryHandler, CallbackQueryHandler,
    ChosenInlineResultHandler,
)

from celery.decorators import task  # to allow event processing to run async

from dtb.settings import TELEGRAM_TOKEN

def setup_dispatcher(dp):
    """
    Adding handlers for events from Telegram
    """

    dp.add_handler(CallbackQueryHandler(reaction_handler, pattern="^r\d+_\d+"))

    dp.add_handler(MessageHandler(
        Filters.chat(chat_id=int(TELEGRAM_FILESTORAGE_ID)),
        # & Filters.forwarded & (Filters.photo | Filters.video | Filters.animation),
        save_forwarded_meme,
    ))

    dp.add_handler(CommandHandler("start", start_handler))
    dp.add_handler(CommandHandler("stats", stats))
    dp.add_handler(CommandHandler("referral", referral))
    dp.add_handler(CommandHandler("settings", language_handler))
    dp.add_handler(CommandHandler("lang", language_handler))
    dp.add_handler(CommandHandler("info", info_handler))
    dp.add_handler(CommandHandler("ads", ads_handler))
    dp.add_handler(CommandHandler("search", search_command))

    dp.add_handler(InlineQueryHandler(search_inline))

    # admin commands
    dp.add_handler(CommandHandler("mod", make_moderator))
    dp.add_handler(CommandHandler("merge", merge_memes_handler))
    dp.add_handler(CommandHandler("show", show_memes))
    dp.add_handler(CommandHandler("source", add_source))
    dp.add_handler(CommandHandler("admin", admin_list))
    dp.add_handler(CommandHandler("search_user", search_user))
    dp.add_handler(CommandHandler("set_lang", set_lang))
    dp.add_handler(CommandHandler("liked", last_user_liked_memes))
    dp.add_handler(CommandHandler("disliked", last_user_disliked_memes))


    dp.add_handler(CallbackQueryHandler(channel_reaction_handler, pattern="^c\d+_\d+"))
    dp.add_handler(CallbackQueryHandler(language_handler, pattern=f"^{LANGUAGE_CALLBACK}"))
    dp.add_handler(CallbackQueryHandler(add_hack_consumer, pattern="^add_hack_consumer"))
    dp.add_handler(CallbackQueryHandler(delete_handler, pattern="^delete"))

    dp.add_handler(ChosenInlineResultHandler(search_chosen_result))

    # dp.add_handler(CallbackQueryHandler(onboarding_handler, pattern="^h\d+"))
    # dp.add_handler(CallbackQueryHandler(ads_handler, pattern="^a\d+_\d+"))

    dp.add_handler(MessageHandler(Filters.text, start_handler))

    dp.add_handler(MessageHandler(
        Filters.document, file_handler,
    ))

    return dp


def run_pooling():
    """ Run bot in pooling mode """
    updater = Updater(TELEGRAM_TOKEN, use_context=True)

    dp = updater.dispatcher
    dp = setup_dispatcher(dp)

    updater.start_polling()
    updater.idle()


@task(ignore_result=True)
def process_telegram_event(update_json):
    update = telegram.Update.de_json(update_json, bot)
    dispatcher.process_update(update)


# Global variable - best way I found to init Telegram bot
bot = telegram.Bot(TELEGRAM_TOKEN)
dispatcher = setup_dispatcher(Dispatcher(bot, None, workers=0, use_context=True))