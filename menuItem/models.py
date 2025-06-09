from django.db import models

class MenuItem(models.Model):
    class Meta:
        verbose_name="ایتم"
        verbose_name_plural="ایتم ها"
    name = models.CharField(max_length=100, verbose_name="نام")
    price = models.IntegerField( verbose_name="قیمت")
    desc = models.CharField(max_length=1000, verbose_name="توضیحات")
    image = models.FileField(upload_to="media/Menu_Item", verbose_name="عکس محصول")

    def __str__(self):
        return str(f"{self.name} -- {self.price}")
