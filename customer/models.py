from django.db import models
from core.models import Core

class Customer(models.Model):
    class Meta:
        verbose_name="مشتری"
        verbose_name_plural="مشتریان"
    name = models.CharField(max_length=100, verbose_name="نام مشتری")
    phone_number = models.IntegerField(verbose_name="شماره تماس مشتری", null=True, blank=True)

    def __str__(self):
        return str(f"{self.name} -- {self.phone_number}")
