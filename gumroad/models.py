from django.db import models

from gumroad import api

class Product(models.Model):
    id = models.CharField(max_length=24, primary_key=True)
    name = models.CharField(max_length=100)
    url = models.URLField(max_length=100, blank=True, null=True)
    preview_url = models.URLField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    customizable_price = models.BooleanField()
    require_shipping = models.BooleanField()
    custom_receipt = models.TextField(blank=True, null=True)
    custom_permalink = models.URLField(max_length=100, blank=True, null=True)
    subscription_duration = models.CharField(max_length=50, blank=True, null=True)
    price = models.PositiveSmallIntegerField(help_text="in cents")
    currency = models.CharField(max_length=10)
    short_url = models.URLField(max_length=100)
    formatted_price = models.CharField(max_length=24)
    published = models.BooleanField()
    shown_on_profile = models.BooleanField()
    file_info = models.JSONField()
    max_purchase_count = models.PositiveSmallIntegerField(blank=True, null=True)
    deleted = models.BooleanField()
    custom_fields = models.JSONField()
    custom_summary = models.TextField(blank=True, null=True)
    variants = models.JSONField()
    sales_count = models.PositiveSmallIntegerField(help_text="in cents")
    sales_usd_cents = models.FloatField()

    @classmethod
    def update(cls):
        products_data = api.get_products()
        if products_data["success"]:
            for product_data in products_data["products"]:
                cls.from_json(product_data)
        return len(products_data["products"])

    @classmethod
    def from_json(cls, d):
        class_fields = set(field.name for field in cls._meta.get_fields())
        data_fields = set(d.keys())
        p, _ = cls.objects.update_or_create(id=d["id"], defaults={k: d[k] for k in class_fields & data_fields})
        return p


class Sale(models.Model):
    id = models.CharField(max_length=24, primary_key=True)
    email = models.EmailField(max_length=100)
    seller_id = models.CharField(max_length=24)
    timestamp = models.CharField(max_length=50)
    daystamp = models.CharField(max_length=50)
    created_at = models.DateTimeField()
    product_name = models.CharField(max_length=100)
    product_has_variants = models.BooleanField()
    price = models.PositiveSmallIntegerField(help_text="in cents")
    gumroad_fee = models.PositiveSmallIntegerField(help_text="in cents")
    formatted_display_price = models.CharField(max_length=24)
    formatted_total_price = models.CharField(max_length=24)
    currency_symbol = models.CharField(max_length=4)
    amount_refundable_in_currency = models.CharField(max_length=4)

    product_id = models.CharField(max_length=24)
    product_permalink = models.CharField(max_length=10)
    refunded = models.BooleanField()
    partially_refunded = models.BooleanField()
    chargedback = models.BooleanField()

    purchase_email = models.EmailField(max_length=100)
    zip_code = models.CharField(max_length=24, blank=True, null=True)
    paid = models.BooleanField()
    has_variants = models.BooleanField()
    variants_and_quantity = models.CharField(max_length=50, blank=True)
    has_custom_fields = models.BooleanField()
    custom_fields = models.JSONField()
    order_id = models.PositiveIntegerField()

    is_product_physical = models.BooleanField()
    is_recurring_billing = models.BooleanField()
    can_contact = models.BooleanField()
    is_following = models.BooleanField()
    is_additional_contribution = models.BooleanField()
    discover_fee_charged = models.BooleanField()
    is_gift_sender_purchase = models.BooleanField()
    is_gift_receiver_purchase = models.BooleanField()

    referrer = models.CharField(max_length=100)
    card = models.JSONField()
    product_rating = models.PositiveSmallIntegerField(blank=True, null=True)
    reviews_count = models.PositiveSmallIntegerField()
    average_rating = models.FloatField()
    quantity = models.PositiveSmallIntegerField()

    @classmethod
    def update(cls):
        sales_data = api.get_sales()
        if sales_data["success"]:
            for sale_data in sales_data["sales"]:
                cls.from_json(sale_data)
        return len(sales_data["sales"])

    @classmethod
    def from_json(cls, d):
        class_fields = set(field.name for field in cls._meta.get_fields())
        data_fields = set(d.keys())
        p, _ = cls.objects.update_or_create(id=d["id"], defaults={k: d[k] for k in class_fields & data_fields})
        return p


class Subscriber(models.Model):
    id = models.CharField(max_length=24, primary_key=True)
    product_id = models.CharField(max_length=24)
    product_name = models.CharField(max_length=100)
    user_id = models.CharField(max_length=24)
    user_email = models.EmailField(max_length=100)
    purchase_ids = models.JSONField()
    created_at = models.DateTimeField()
    cancelled_at = models.DateTimeField(blank=True, null=True)
    user_requested_cancellation_at = models.DateTimeField(blank=True, null=True)
    charge_occurrence_count = models.PositiveSmallIntegerField(blank=True, null=True)
    recurrence = models.CharField(max_length=20)
    ended_at = models.DateTimeField(blank=True, null=True)

    @classmethod
    def update(cls):
        for p in Product.objects.filter(subscription_duration__isnull=False).all():
            res = api.get_subscribers(p.id)
            if res["success"]:
                for s in res["subscribers"]:
                    cls.from_json(s)
    
    @classmethod
    def from_json(cls, d):
        class_fields = set(field.name for field in cls._meta.get_fields())
        data_fields = set(d.keys())
        p, _ = cls.objects.update_or_create(id=d["id"], defaults={k: d[k] for k in class_fields & data_fields})
        return p