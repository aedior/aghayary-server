from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Core(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=User, verbose_name="ساخته شده توسط")