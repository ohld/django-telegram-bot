import json
import logging
from django.views import View
from django.shortcuts import redirect
from django.http import JsonResponse

from dtb.settings import DEBUG

from tgbot import tasks
from tgbot.models import User, Payment
from tgbot.handlers.logs import send_text
from tgbot.handlers.dispatcher import process_telegram_event, TELEGRAM_BOT_USERNAME

from gumroad.models import Sale

logger = logging.getLogger(__name__)

BOT_URL = f"https://t.me/{TELEGRAM_BOT_USERNAME}"


def index(request):
    return JsonResponse({"error": "sup hacker"})


class TelegramBotWebhookView(View):
    # WARNING: if fail - Telegram webhook will be delivered again. 
    # Can be fixed with async celery task execution
    def post(self, request, *args, **kwargs):
        if DEBUG:
            process_telegram_event(json.loads(request.body))
        else:  # use celery in production
            process_telegram_event.delay(json.loads(request.body))

        # TODO: there is a great trick to send data in webhook response
        # e.g. remove buttons
        return JsonResponse({"ok": "POST request processed"})
    
    def get(self, request, *args, **kwargs):  # for debug
        return JsonResponse({"ok": "Get request processed. But nothing done"})


class PaymentRedirect(View):
    # https://help.gumroad.com/article/154-custom-delivery-products
    def get(self, request, *args, **kwargs):  # for debug
        print(f"Received params: {request.GET}")
        params = request.GET.dict()
        if len(params) == 0:  # not ours callback
            return redirect(BOT_URL)

        sale_id = params.get('sale_id')
        product_id = params.get('product_id')
        # params.get('product_permalink')

        if sale_id is None:
            logger.error(f"Strange GET data passed: {params}")
            return redirect(BOT_URL)

        Sale.update()

        # get sale data
        sale = Sale.objects.filter(id=sale_id).first()
        if sale is None:
            logger.error(f"strange sale_id={sale_id}")
            return redirect(BOT_URL)

        if not sale.paid:
            logger.error(f"Sale {sale} was not paid yet, skipping.")
            return redirect(BOT_URL)

        user_id = sale.custom_fields.get("client_id")
        if user_id is None:
            send_text(f"New payment but without client_id. [Gumroad](https://gumroad.com/customers)")
            return redirect(BOT_URL)

        u = User.objects.filter(user_id=user_id).first()
        if u is None:
            send_text(f"New payment but with invalid client_id={user_id}. [Gumroad](https://gumroad.com/customers)")
            return redirect(BOT_URL)

        try:
            p, created = Payment.objects.get_or_create(user=u, product_id=product_id, sale_id=sale_id)
        except Exception as e:
            logger.error(f"Can't create Payment, reason: {e}")
            return redirect(BOT_URL)

        if created:  # acces not yet given
            if product_id == "????????==":  # add product_id
                pass
            else:  # not our product
                return redirect(BOT_URL)

            send_text(f"""
🤑 User {u} purchased {sale.product_name}! (+${(sale.price - sale.gumroad_fee)/100}).
            """)

        tasks.send_payment_confirmation.delay(user_id)
        return redirect(BOT_URL)
