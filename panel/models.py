from django.db import models

class PanelModel(models.Model):
    class Meta:
        verbose_name="پنل"
        verbose_name_plural="پنل"
    order_item = models.ForeignKey("order.OrderItem", on_delete=models.CASCADE, verbose_name="آیتم سفارش")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="زمان ثبت")

    @property
    def customer(self):
        return self.order_item.order.customer

    @property
    def menu_item(self):
        return self.order_item.menu_item

    @property
    def quantity(self):
        return self.order_item.quantity

    @property
    def price_buy(self):
        return self.menu_item.price_shop

    @property
    def price_sell(self):
        return self.menu_item.price

    @property
    def profit(self):
        return (self.price_sell - self.price_buy) * self.quantity

    def __str__(self):
        return f"پنل: {self.menu_item.name} برای {self.customer.name} در {self.created_at}"
