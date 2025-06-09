from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Order
from persiantools.jdatetime import JalaliDateTime

def invoice_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    jalali_date = JalaliDateTime(order.created_at).strftime("%Y/%m/%d - %H:%M")
    return render(request, 'invoice.html', {
        'order': order,
        'jalali_date': jalali_date,
    })
