from django.db import models

class MenuItem(models.Model):
    class Meta:
        verbose_name="ایتم"
        verbose_name_plural="ایتم ها"
    name = models.CharField(max_length=100, verbose_name="نام")
    price_shop = models.IntegerField( verbose_name="قیمت خرید")
    price = models.IntegerField( verbose_name="قیمت فروش")
    count = models.IntegerField(verbose_name="تعداد موجود")
    
    def __str__(self):
        return str(f"{self.name} -- {self.price}")
