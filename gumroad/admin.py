from django.contrib import admin
from django.http import HttpResponseRedirect

from gumroad.models import Product, Sale, Subscriber
from gumroad.api import get_products, get_sales


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'price', 'sales_count', 'sales_usd_cents', 'published', 
    ]

    actions = ["sync_data"]

    def sync_data(self, request, queryset):
        # ignore queryset for now, update everything
        n_updated = Product.update()
        self.message_user(request, f"Updated {n_updated} products.")
        return HttpResponseRedirect(request.get_full_path())


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = [
        "id", "email", "product_name", "paid", "refunded", "created_at"
    ]

    actions = ["sync_data"]

    def sync_data(self, request, queryset):
        # ignore queryset for now, update everything
        n_updated = Sale.update()
        self.message_user(request, f"Updated {n_updated} sales.")
        return HttpResponseRedirect(request.get_full_path())


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'product_id', 'product_name', 'user_email', 'created_at', "recurrence", "cancelled_at", 
    ]

    actions = ["sync_data"]

    def sync_data(self, request, queryset):
        # ignore queryset for now, update everything
        _ = Subscriber.update()
        self.message_user(request, f"Subscribers were updated.")
        return HttpResponseRedirect(request.get_full_path())