from django.db import models
from core.models import Core
# Create your models here.
class Expend(Core):
    class Meta:
        verbose_name="هزینه"
        verbose_name_plural="هزینه ها"
    count = models.IntegerField(verbose_name="مقدار به تومان")
    desc = models.CharField(max_length=1000, verbose_name="توضیحات", null=True, blank=True)
    image = models.ImageField(null=True,blank=True,verbose_name="عکس فاکتور")