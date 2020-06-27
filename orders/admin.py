from django.contrib import admin
from .models import Item, Cart, ItemOrder
from .models import Item, dishType, Cart, ItemOrder, ToppingsPrice
from django.db import models

class ItemInline(admin.TabularInline):
    model = ItemOrder
    # no need extra forms for adding new item orders
    extra = 0
    filter_horizontal = ('toppings',)

    class Media:
        css = {
            'all': ('css/style.css',),
        }

class AdiminCart(admin.ModelAdmin):
    inlines = (ItemInline,)
    readonly_fields = ['user', 'order_date']

    # filter by user name and order number
    search_fields = (
        "user__username", "id"
    )

class AdminItem(admin.ModelAdmin):
    # filter by name
    search_fields = (
        "name", "group__dishType",
    )


admin.site.register(Item, AdminItem)
admin.site.register(dishType)
admin.site.register(Cart, AdiminCart)
admin.site.register(ItemOrder)
admin.site.register(ToppingsPrice)
