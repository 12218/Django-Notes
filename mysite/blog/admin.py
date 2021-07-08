from django.contrib import admin
# from .models import BlogType, Blog, ReadNum # 引入创建好的博客模型和博客分类、阅读量
from .models import BlogType, Blog # 引入创建好的博客模型和博客分类、阅读量

# 在此进行博客模型的注册
# Register your models here.
@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin): # 注册博客分类
    list_display = ('id', 'type_name') # 此处放入的值为在超级管理员界面显示的信息

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin): # 注册博客模型
    # list_display = ('title', 'blog_type', 'author', 'get_read_num', 'create_time', 'last_updated_time') # 此处放入的值为在超级管理员界面显示的信息
    list_display = ('id', 'title', 'blog_type', 'author', 'get_read_num', 'create_time', 'last_updated_time') # 此处放入的值为在超级管理员界面显示的信息

'''
@admin.register(ReadNum)
class BlogAdmin(admin.ModelAdmin): # 注册阅读量模型
    list_display = ('read_num', 'blog')
'''