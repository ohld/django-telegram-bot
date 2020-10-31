from django.contrib import admin

from .models import Pornstar, PornstarVideo, Video, Similar

@admin.register(Pornstar)
class PornstarAdmin(admin.ModelAdmin):
    list_display = [
        "pornstar_id", "link", "rank", "subscribers", "views",
    ]
    actions = ["update"]

    def update(self, request, queryset):
        for i in queryset:
            i.update()


@admin.register(PornstarVideo)
class PornstarVideoAdmin(admin.ModelAdmin):
    list_display = [
        "id", "pornstar", "video",
    ]


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = [
        "video_id", "link", "title", "views",
    ]


@admin.register(Similar)
class SimilarAdmin(admin.ModelAdmin):
    list_display = [
        "id", "pornstar", "similar_to",
    ]