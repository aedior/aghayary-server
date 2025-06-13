from django.db import models
from django.utils import timezone
from customer.models import Customer
from menuItem.models import MenuItem
from django_jalali.admin import jDateTimeField
from core.models import Core





class Order(Core):
    class Meta:
        verbose_name="سفارش"
        verbose_name_plural="سفارش ها"
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="مشتری", related_name="customer_order")
    created_at = jDateTimeField(auto_now_add=True, verbose_name="زمان")
    discount = models.IntegerField(default=0, verbose_name="تخفیف")



    @property
    def createdat(self):
        return self.created_at.strftime("%Y-%m-%d %H:%M")

    def total_price(self):
        if self.discount > 0:
            return (sum(item.total_price() for item in self.items.all()) - self.discount)
        else:
            return sum(item.total_price() for item in self.items.all())

    def __str__(self):
        return f"Order #{self.id} by {self.customer.name}"


class OrderItem(models.Model):
    class Meta:
        verbose_name="ایتم سفارش"
        verbose_name_plural="ایتم های سفارش"
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name="سفارش")
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, verbose_name="ایتم منو",related_name="menu_order")
    quantity = models.PositiveIntegerField(default=1, verbose_name="تعداد")

    def total_price(self):
        return self.menu_item.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name}"
