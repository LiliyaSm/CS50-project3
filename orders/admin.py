from django.contrib import admin
from .models import Item, Cart, ItemOrder
from .models import Item, dishType, Cart, ItemOrder
 
class ItemInline(admin.TabularInline):
    model = ItemOrder
    # no adding extra forms
    extra = 0
    # readonly_fields = ['subtotal']
    # exclude = ['price']

# Register your models here.


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
    inlines = (ItemInline,)
    # filter by name
    search_fields = (
        "item__name", "item__group",
    )


admin.site.register(Item, AdminItem)
admin.site.register(dishType)
admin.site.register(Cart, AdiminCart)
admin.site.register(ItemOrder)
