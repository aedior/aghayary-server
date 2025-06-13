# accounting/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from expend.models import Expend
from panel.models import PanelModel  # مسیر دقیق مدل پنل شما
from django.utils.timezone import now

@receiver(post_save, sender=Expend)
def create_panel_for_expend(sender, instance, created, **kwargs):
    if created:
        PanelModel.objects.create(
            expend=instance,
            created_at=now(),  # یا instance.created_at اگر موجود باشد
        )
