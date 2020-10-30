import json
from django.views import View
from django.http import JsonResponse

# from telegram import Update

# from tgbot.bot.bot import dispatcher, bot
# from tgbot.bot.tasks import process_telegram_event


def index(request):
    return JsonResponse({"error": "sup hacker"})


class TelegramBotWebhookView(View):
    def post(self, request, *args, **kwargs):
        process_telegram_event(json.loads(request.body))
        # process_telegram_event.delay(json.loads(request.body))
        # update = Update.de_json(json.loads(request.body), bot)
        # dispatcher.process_update(update)

        # TODO: there is a great trick to send data in webhook response

        return JsonResponse({"ok": "POST request processed"})
    
    def get(self, request, *args, **kwargs):
        return JsonResponse({"ok": "Get request processed. But nothing done"})