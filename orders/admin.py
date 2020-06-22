from django.contrib import admin
from .models import Item, Cart, ItemOrder
from .models import Item, dishType, Cart, ItemOrder, ToppingsPrice
from django.db import models

class ItemInline(admin.TabularInline):
    model = ItemOrder
    # no need extra forms for adding new item orders
    extra = 0
    # readonly_fields = ['subtotal']
    # exclude = ['price']
    filter_horizontal = ('toppings',)
    
    # def get_fields(self, request, obj=None):
    #     # if self.model.objects.all()[0].toppings.all() is None:
    #     #     return ("item")
    #     print(obj.products.all())
    #     return ('item', 'toppings')


    # fieldsets = (
    #     (None, {
    #         'fields': ('item', 'topping')
    #     }),
    # )


    class Media:
        css = {
            # if you have saved this file in `static/css/` then the path must look like `('css/resize-widget.css',)`
            'all': ('css/style.css',),
        }

class AdiminCart(admin.ModelAdmin):
    inlines = (ItemInline,)
    fieldsets = (
        (None, {
            'fields': ('user', 'total')
        }),
    )

    # filter by name
    search_fields = (
        "user__username",
    )

 #list_filter



class AdminItem(admin.ModelAdmin):
    # inlines = (ItemInline,)
    # filter by name
    search_fields = (
        "name", "group__dishType",
    )


admin.site.register(Item, AdminItem)
admin.site.register(dishType)
admin.site.register(Cart, AdiminCart)
admin.site.register(ItemOrder)
admin.site.register(ToppingsPrice)
