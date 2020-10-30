import json
from django.views import View
from django.http import JsonResponse

from tgbot.handlers.dispatcher import process_telegram_event


def index(request):
    return JsonResponse({"error": "sup hacker"})


class TelegramBotWebhookView(View):
    def post(self, request, *args, **kwargs):
        process_telegram_event(json.loads(request.body))

        # TODO: there is a great trick to send data in webhook response
        return JsonResponse({"ok": "POST request processed"})
    
    def get(self, request, *args, **kwargs):  # for debug
        return JsonResponse({"ok": "Get request processed. But nothing done"})