from django.contrib import admin
from .models import Expend

# Register your models here.

@admin.register(Expend)
class ExpendAdmin(admin.ModelAdmin):
    list_display=['count','desc','image','created_by']