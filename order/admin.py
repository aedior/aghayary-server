from django.contrib import admin
from .models import  Order, OrderItem
from django.urls import reverse
from django.utils.html import format_html
from django_jalali.admin import jDateTimeField
from django_jalali.admin.filters import JDateFieldListFilter

# You need to import this for adding jalali calendar widget
import django_jalali.admin as jadmin

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = ['total_price']

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'createdat', 'total_price_display', 'dis', 'invoice_link', 'created_by', "method")
    list_filter = (
        ('created_at', JDateFieldListFilter),
        'customer',
        "method"
    )
    inlines = [OrderItemInline]

    def total_price_display(self, obj):
        return f"{obj.total_price():,.0f} تومان"
    total_price_display.short_description = 'جمع کل'

    def dis(self, obj):
        return f"{obj.discount:,.0f} تومان"
    dis.short_description = 'تخفیف'


    def invoice_link(self, obj):
        url = reverse('order-invoice', args=[obj.id])
        return format_html('<a class="button" href="{}" target="_blank">فاکتور</a>', url)
    invoice_link.short_description = 'فاکتور'

admin.site.register(Order, OrderAdmin)
