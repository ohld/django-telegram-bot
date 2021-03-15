import random
import telegram
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import render

from dtb.settings import DEBUG

from tgbot.models import Location, Arcgis
from tgbot.models import User, UserActionLog
from tgbot.forms import BroadcastForm
from tgbot.handlers import utils

from tgbot.tasks import broadcast_message

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'user_id', 'username', 'first_name', 'last_name', 
        'language_code', 'deep_link',
        'created_at', 'updated_at', "is_blocked_bot",
    ]
    list_filter = ["is_blocked_bot", "is_moderator"]
    search_fields = ('username', 'user_id')

    actions = ['broadcast']

    def invited_users(self, obj):
        return obj.invited_users().count()

    def broadcast(self, request, queryset):
        """ Select users via check mark in django-admin panel, then select "Broadcast" to send message"""
        if 'apply' in request.POST:
            broadcast_message_text = request.POST["broadcast_text"]

            # TODO: for all platforms?
            if len(queryset) <= 3 or DEBUG:  # for test / debug purposes - run in same thread
                for u in queryset:
                    utils.send_message(user_id=u.id, text=broadcast_message_text, parse_mode=telegram.ParseMode.MARKDOWN)
                self.message_user(request, "Just broadcasted to %d users" % len(queryset))
            else:
                user_ids = list(set(u.user_id for u in queryset))
                random.shuffle(user_ids)
                broadcast_message.delay(message=broadcast_message_text, user_ids=user_ids)
                self.message_user(request, "Broadcasting of %d messages has been started" % len(queryset))

            return HttpResponseRedirect(request.get_full_path())

        form = BroadcastForm(initial={'_selected_action': queryset.values_list('user_id', flat=True)})
        return render(
            request, "admin/broadcast_message.html", {'items': queryset,'form': form, 'title':u' '}
        )

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'created_at']


@admin.register(Arcgis)
class ArcgisAdmin(admin.ModelAdmin):
    list_display = ['location', 'city', 'country_code']


@admin.register(UserActionLog)
class UserActionLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'created_at']