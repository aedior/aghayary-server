from django.db import models
from core.models import Core
from django.contrib.auth.models import User
from django_jalali.admin import jDateTimeField


class MenuItem(Core):
    class Meta:
        verbose_name="ایتم"
        verbose_name_plural="ایتم ها"
    name = models.CharField(max_length=100, verbose_name="نام")
    price_shop = models.IntegerField( verbose_name="قیمت خرید")
    price = models.IntegerField( verbose_name="قیمت فروش")
    count = models.IntegerField(verbose_name="تعداد موجود")
    

    def profit(self):
        return (self.price - self.price_shop)
    
    def __str__(self):
        return str(f"{self.name} -- {self.price}")



class MenuItemcount(models.Model):
    class Meta:
        verbose_name="تعداد افزودنی"
        verbose_name_plural="تعداد افزودنی ها"
    Item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, verbose_name="محصول مربوطه")
    count = models.IntegerField(verbose_name="تعداد ورودی شما")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=User, verbose_name="ساخته شده توسط")
    created_at = jDateTimeField(auto_now_add=True, verbose_name="زمان")

    def createdat(self):
        return self.created_at.strftime("%Y-%m-%d %H:%M")

    def save(self, *args, **kwargs):
        # بررسی اینکه آیا این عمل قبلاً انجام شده یا نه
        exists = MenuItemcount.objects.filter(
            Item=self.Item,
            count=self.count,
            created_at=self.created_at
        ).exists()

        if not exists:
            # افزودن count جدید به count موجود در MenuItem
            self.Item.count += self.count
            self.Item.save()

        super().save(*args, **kwargs)