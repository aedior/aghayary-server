from django.contrib import admin
from .models import MenuItem,MenuItemcount


class CountItemInline(admin.TabularInline):
    model = MenuItemcount
    extra = 0
    readonly_fields = ['createdat']

@admin.register(MenuItem)
class ItemAdmin(admin.ModelAdmin):
    list_display=['name','priceshop','pricesell', 'count','profit','created_by']
    inlines=[CountItemInline]
    def profit(self, obj):
        profit = obj.price - obj.price_shop
        return f"{profit:,.0f} تومان"
    profit.short_description = "سود خالص"

    def priceshop(self, obj):
        return f"{obj.price_shop:,.0f} تومان"
    priceshop.short_description = 'قیمت خرید'

    def pricesell(self, obj):
        return f"{obj.price:,.0f} تومان"
    pricesell.short_description = 'قیمت فروش'
