
# Create your views here.
import openpyxl
from collections import defaultdict
from django.http import HttpResponse
from .models import PanelModel

def export_panels_excel(request):
    # آماده‌سازی داده‌ها با گروه‌بندی بر اساس menu_item
    grouped_data = defaultdict(lambda: {
        'name': '',
        'quantity': 0,
        'price_buy': 0,
        'price_sell': 0,
        'profit': 0,
    })

    panels = PanelModel.objects.select_related('order_item__order', 'order_item__menu_item')

    for panel in panels:
        key = panel.menu_item.id  # می‌تونی از ترکیب فیلدها هم استفاده کنی
        grouped_data[key]['name'] = panel.menu_item.name
        grouped_data[key]['quantity'] += panel.quantity
        grouped_data[key]['price_buy'] += panel.price_buy * panel.quantity
        grouped_data[key]['price_sell'] += panel.price_sell * panel.quantity
        grouped_data[key]['profit'] += panel.profit

    # ایجاد فایل اکسل
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "پنل‌ها"

    # هدر
    ws.append(['نام آیتم', 'تعداد', 'جمع خرید', 'جمع فروش', 'سود'])

    total_quantity = 0
    total_buy = 0
    total_sell = 0
    total_profit = 0

    for item in grouped_data.values():
        ws.append([
            item['name'],
            item['quantity'],
            item['price_buy'],
            item['price_sell'],
            item['profit'],
        ])
        total_quantity += item['quantity']
        total_buy += item['price_buy']
        total_sell += item['price_sell']
        total_profit += item['profit']

    # ردیف جمع کل
    ws.append(['جمع کل', total_quantity, total_buy, total_sell, total_profit])

    # پاسخ HTTP برای دانلود فایل
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=panels_summary.xlsx'
    wb.save(response)
    return response
