from django.db import models
from django.utils import timezone
from customer.models import Customer
from menuItem.models import MenuItem

class Order(models.Model):
    class Meta:
        verbose_name="سفارش"
        verbose_name_plural="سفارش ها"
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="مشتری")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="زمان")

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())

    def __str__(self):
        return f"Order #{self.id} by {self.customer.name}"


class OrderItem(models.Model):
    class Meta:
        verbose_name="ایتم سفارش"
        verbose_name_plural="ایتم های سفارش"
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name="سفارش")
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, verbose_name="ایتم منو")
    quantity = models.PositiveIntegerField(default=1, verbose_name="تعداد")

    def total_price(self):
        return self.menu_item.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name}"
