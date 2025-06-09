from django.db.models.signals import post_save
from django.dispatch import receiver
from order.models import OrderItem
from panel.models import PanelModel # فرض بر اینکه PanelModel توی اپ panel هست
from menuItem.models import MenuItem

@receiver(post_save, sender=OrderItem)
def update_menu_item_and_panel(sender, instance, created, **kwargs):
    menu_item = instance.menu_item
    order_quantity = instance.quantity

    if created:
        # کم کردن تعداد موجود از MenuItem
        menu_item.count -= order_quantity
        menu_item.save()

        # ایجاد رکورد در PanelModel
        PanelModel.objects.create(order_item=instance)
