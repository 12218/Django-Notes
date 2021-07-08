from django.contrib import admin
from .models import ReadNum

# Register your models here.
@admin.register(ReadNum)
class ReadNumAdmin(admin.ModelAdmin): # 注册阅读量模型
    list_display = ('read_num', 'content_object')