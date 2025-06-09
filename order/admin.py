from django.contrib import admin
from .models import  Order, OrderItem
from django.urls import reverse
from django.utils.html import format_html

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = ['total_price']

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'created_at', 'total_price_display', 'invoice_link')
    inlines = [OrderItemInline]

    def total_price_display(self, obj):
        return f"{obj.total_price():,.0f} تومان"
    total_price_display.short_description = 'جمع کل'


    def invoice_link(self, obj):
        url = reverse('order-invoice', args=[obj.id])
        return format_html('<a class="button" href="{}" target="_blank">فاکتور</a>', url)
    invoice_link.short_description = 'فاکتور'

admin.site.register(Order, OrderAdmin)
