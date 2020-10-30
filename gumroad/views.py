import json
from django.views import View
from django.http import JsonResponse

from gumroad.models import Sale

class GumroadPingWebhook(View):
    # https://gumroad.com/ping
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        Sale.update()
        print(f"Just received Ping data from Gumroad: {data}")

        return JsonResponse({"ok": "POST request processed"})
    
    def get(self, request, *args, **kwargs):  # for debug
        return JsonResponse({"ok": "Get request processed. But nothing done"})