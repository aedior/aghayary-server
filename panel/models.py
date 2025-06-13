from django.db import models
from django_jalali.admin import jDateTimeField


class PanelModel(models.Model):
    class Meta:
        verbose_name="پنل"
        verbose_name_plural="پنل"
    order_item = models.ForeignKey("order.OrderItem", on_delete=models.CASCADE, verbose_name="آیتم سفارش", null=True, blank=True,)
    created_at = jDateTimeField(auto_now_add=True, verbose_name="زمان ثبت")
    expend = models.OneToOneField("expend.Expend", on_delete=models.CASCADE, null=True, blank=True, verbose_name="هزینه مرتبط")

    @property
    def createdat(self):
        return self.created_at.strftime("%Y-%m-%d %H:%M")

    @property
    def customer(self):
        if self.order_item:
            return self.order_item.order.customer
        
    @property
    def menu_item(self):
        if self.order_item:
            return self.order_item.menu_item

    @property
    def quantity(self):
        if self.order_item:
            return self.order_item.quantity

    @property
    def price_buy(self):
        if self.order_item:
            return self.menu_item.price_shop

    @property
    def price_sell(self):
        if self.order_item:
            return self.menu_item.price

    @property
    def profit(self):
        if self.order_item:
            return ((self.price_sell - self.price_buy) * self.quantity)-self.order_item.order.discount
        else:
            return self.expend.count

    def __str__(self):
        if self.order_item:
            return f"پنل: {self.menu_item.name} برای {self.customer.name} در {self.created_at}"
        else:
            return f"{self.expend.count} هزینه:"