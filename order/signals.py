from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import OrderItem
from menuItem.models import MenuItem
from panel.models import PanelModel

# این دیکشنری برای ذخیره مقدار قبلی quantity قبل از ذخیره استفاده می‌شود
_prev_quantities = {}

@receiver(pre_save, sender=OrderItem)
def cache_previous_quantity(sender, instance, **kwargs):
    if instance.pk:
        try:
            prev_instance = OrderItem.objects.get(pk=instance.pk)
            _prev_quantities[instance.pk] = prev_instance.quantity
        except OrderItem.DoesNotExist:
            _prev_quantities[instance.pk] = 0

@receiver(post_save, sender=OrderItem)
def update_menu_item_and_panel(sender, instance, created, **kwargs):
    menu_item = instance.menu_item

    if created:
        # برای ایجاد جدید، فقط کم می‌کنیم
        menu_item.count -= instance.quantity
        menu_item.save()

        # ایجاد رکورد در PanelModel
        PanelModel.objects.create(order_item=instance)
    else:
        # محاسبه تفاوت بین مقدار قبلی و جدید
        old_quantity = _prev_quantities.get(instance.pk, 0)
        quantity_diff = instance.quantity - old_quantity

        # اگر quantity افزایش یافته، count باید بیشتر کم شود
        # اگر کاهش یافته، count باید جبران شود
        menu_item.count -= quantity_diff
        menu_item.save()

    # پاک‌سازی cache
    if instance.pk in _prev_quantities:
        del _prev_quantities[instance.pk]


from django.db.models.signals import post_delete

@receiver(post_delete, sender=OrderItem)
def restore_menu_item_on_delete(sender, instance, **kwargs):
    menu_item = instance.menu_item
    menu_item.count += instance.quantity  # بازگرداندن موجودی
    menu_item.save()
