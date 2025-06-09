from django.contrib import admin
from .models import PanelModel
from collections import defaultdict
import openpyxl
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import cidfonts
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_RIGHT
import os
from django.conf import settings
import arabic_reshaper
from bidi.algorithm import get_display


@admin.register(PanelModel)
class PanelModelAdmin(admin.ModelAdmin):
    list_display = [
        'menu_item_name',
        'customer_name',
        'quantity',
        'price_buy',
        'price_sell',
        'profit',
        'created_at',
    ]
    readonly_fields = [
        'menu_item_name',
        'customer_name',
        'quantity',
        'price_buy',
        'price_sell',
        'profit',
        'created_at',
    ]
    list_filter = ['created_at']
    search_fields = ['order_item__menu_item__name', 'order_item__order__customer__name']
    ordering = ['-created_at']

    actions = ["export_to_pdf"]

    @admin.action(description="خروجی PDF ")
    def export_to_pdf(self, request, queryset):
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.lib.enums import TA_RIGHT
        from reportlab.lib import colors

        font_path = os.path.join(settings.BASE_DIR, "panel", "font", "Vazirmatn-Medium.ttf")
        pdfmetrics.registerFont(TTFont("Vazir", font_path))

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=آمار.pdf'

        doc = SimpleDocTemplate(response, pagesize=A4, rightMargin=20, leftMargin=20, topMargin=20, bottomMargin=20)

        style_rtl = ParagraphStyle(
            name='RightAlign',
            fontName='Vazir',
            fontSize=10,
            leading=12,
            alignment=TA_RIGHT,
        )

        def reshape(text):
            return get_display(arabic_reshaper.reshape(str(text)))

        grouped_data = defaultdict(lambda: {
            'name': '',
            'quantity': 0,
            'price_buy_unit': 0,
            'price_sell_unit': 0,
            'price_buy_total': 0,
            'price_sell_total': 0,
            'profit': 0,
        })

        queryset = queryset.select_related('order_item__order', 'order_item__menu_item')

        for panel in queryset:
            key = panel.menu_item.id
            grouped_data[key]['name'] = panel.menu_item.name
            grouped_data[key]['quantity'] += panel.quantity
            grouped_data[key]['price_buy_unit'] = panel.price_buy
            grouped_data[key]['price_sell_unit'] = panel.price_sell
            grouped_data[key]['price_buy_total'] += panel.price_buy * panel.quantity
            grouped_data[key]['price_sell_total'] += panel.price_sell * panel.quantity
            grouped_data[key]['profit'] += panel.profit

        data = [[
            Paragraph(reshape("نام آیتم"), style_rtl),
            Paragraph(reshape("قیمت خرید واحد"), style_rtl),
            Paragraph(reshape("قیمت فروش واحد"), style_rtl),
            Paragraph(reshape("تعداد"), style_rtl),
            Paragraph(reshape("جمع خرید"), style_rtl),
            Paragraph(reshape("جمع فروش"), style_rtl),
            Paragraph(reshape("سود"), style_rtl),
        ]]

        total_quantity = 0
        total_buy = 0
        total_sell = 0
        total_profit = 0

        for item in grouped_data.values():
            data.append([
                Paragraph(reshape(item['name']), style_rtl),
                Paragraph(reshape(item['price_buy_unit']), style_rtl),
                Paragraph(reshape(item['price_sell_unit']), style_rtl),
                Paragraph(reshape(item['quantity']), style_rtl),
                Paragraph(reshape(item['price_buy_total']), style_rtl),
                Paragraph(reshape(item['price_sell_total']), style_rtl),
                Paragraph(reshape(item['profit']), style_rtl),
            ])
            total_quantity += item['quantity']
            total_buy += item['price_buy_total']
            total_sell += item['price_sell_total']
            total_profit += item['profit']

        data.append([
            Paragraph(reshape("جمع کل"), style_rtl),
            "", "", 
            Paragraph(reshape(total_quantity), style_rtl),
            Paragraph(reshape(total_buy), style_rtl),
            Paragraph(reshape(total_sell), style_rtl),
            Paragraph(reshape(total_profit), style_rtl),
        ])

        table = Table(data, colWidths=[75] * 7, hAlign='RIGHT')
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Vazir'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))

        elements = [table]
        doc.build(elements)
        return response


    def menu_item_name(self, obj):
        return obj.menu_item.name
    menu_item_name.short_description = 'نام آیتم'

    def customer_name(self, obj):
        return obj.customer.name
    customer_name.short_description = 'مشتری'

    def quantity(self, obj):
        return obj.quantity
    quantity.short_description = 'تعداد'

    def price_buy(self, obj):
        return obj.price_buy
    price_buy.short_description = 'قیمت خرید'

    def price_sell(self, obj):
        return obj.price_sell
    price_sell.short_description = 'قیمت فروش'

    def profit(self, obj):
        return obj.profit
    profit.short_description = 'سود خالص'
