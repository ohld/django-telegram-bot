from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [  
    path('gumroad_ping_webhook/', csrf_exempt(views.GumroadPingWebhook.as_view())),
]