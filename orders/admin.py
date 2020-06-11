from django.contrib import admin

from .models import Item, dishType, Cart, ItemOrder
# Register your models here.

admin.site.register(Item)
admin.site.register(dishType)
admin.site.register(Cart)
admin.site.register(ItemOrder)
