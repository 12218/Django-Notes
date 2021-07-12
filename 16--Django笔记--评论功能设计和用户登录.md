# 16--Django笔记--评论功能设计和用户登录

## 一、创建评论模型

评论模型中需要应用到的部分包括：

- 评论对象
- 评论内容
- 评论时间
- 评论者

首先使用命令创建评论应用：

```bash
python3 manage.py startapp comment
```

创建模型：

```python
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

# Create your models here.
class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.TextField() # 评论内容
    comment_time = models.DateTimeField(auto_now_add = True) # 评论时间
    user = models.ForeignKey(User, on_delete = models.DO_NOTHING) # 评论者
```

注册应用：

```python
from django.contrib import admin
from .models import Comment

# Register your models here.
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content_object', 'text', 'comment_time', 'user')
```

**setting.py** 中注册应用：

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',
    'ckeditor',
    'ckeditor_uploader',
    'read_statistics',
    'comment',
]
```

最后，迁移数据库

## 二、设计判读用户登录部分

request中有一个属性是user

![16-01](https://img-blog.csdnimg.cn/2021071222375065.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NDMzODc4MA==,size_16,color_FFFFFF,t_70#pic_center)


[用户登录文档](https://docs.djangoproject.com/zh-hans/3.2/topics/auth/default/#authentication-in-web-requests)

![16-02](https://img-blog.csdnimg.cn/20210712223806991.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NDMzODc4MA==,size_16,color_FFFFFF,t_70#pic_center)


在前端页面中添加登录判断：

```html
<div class="row">
            <div class="col-xs-10 col-xs-offset-1">
                <div style="margin-top: 2em; border: 1px dashed; padding: 2em;">
                    提交评论区
                    {% if user.is_authenticated %}
                        用户已登录
                    {% else %}
                        用户未登录
                        <form action="{% url 'login' %}" method="POST">
                            <input type="text" name="username">
                            <input type="password" name="password">
                            <input type="submit" value="登录">
                        </form>
                    {% endif %}
                </div>
                <div style="margin-top: 2em; border: 1px dashed; padding: 2em;">评论列表区</div>
            </div>
        </div>
```

添加登录的url和方法：

**urls.py**

```python
urlpatterns = [
    # path('', blog_list, name = 'home'), # 设置首页
    path('', views.home, name = 'home'),
    path('admin/', admin.site.urls),
    path('ckeditor', include('ckeditor_uploader.urls')),
    path('blog/', include('blog.urls')), # include 方法是将别处的urls路由配置引入到全局路由
    path('login/', views.login, name = 'login'),
]
```

**views.py**

```python
from django.shortcuts import render, redirect
from read_statistics.utils import get_seven_days_read_data, get_today_hot_data, get_yesterday_hot_data # , get_7_days_hot_data
from django.contrib.contenttypes.models import ContentType
from blog.models import Blog
import datetime
from django.core.cache import cache
from django.utils import timezone
from django.db.models import Sum
from django.contrib import auth

def get_7_days_blogs():
    today = timezone.now().date() # 取出今天的日期
    seven_date = today - datetime.timedelta(days = 7)
    blogs = Blog.objects.filter(read_details__date__lt = today, read_details__date__gte = seven_date)\
        .values('id', 'title')\
        .annotate(read_num_sum = Sum('read_details__read_num'))\
        .order_by('-read_num_sum')
    return blogs

def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read_data(blog_content_type) # 获取过去7天阅读数量数组

    # 获取7天热门博客的缓存数据
    hot_blogs_for_7_days = cache.get('hot_blogs_for_7_days')
    if hot_blogs_for_7_days is None:
        hot_blogs_for_7_days = get_7_days_blogs()
        cache.set('hot_blogs_for_7_days', hot_blogs_for_7_days, 3600)
    #     print('set cache')
    # else:
    #     print('use cache')

    today_hot_data = get_today_hot_data(blog_content_type) # 获取今日阅读数据
    yesterday_hot_data = get_yesterday_hot_data(blog_content_type) # 获取昨日阅读数据
    hot_blogs_for_7_days = get_7_days_blogs() # 过去7天的阅读数据

    context = {}
    context['dates'] = dates
    context['read_nums'] = read_nums # 将阅读数组传入前端页面
    context['today_hot_data'] = today_hot_data
    context['yesterday_hot_data'] = yesterday_hot_data
    context['hot_blogs_for_7_days'] = hot_blogs_for_7_days
    return render(request, 'home.html', context)


def login(request):
    username = request.POST.get('username', '') # 从request中取出username字段，如果没有则设为空字符串
    password = request.POST.get('password', '')

    user = auth.authenticate(request, username = username, password = password) # 获取登录信息
    if user is not None:
        auth.login(request, user)
        return redirect('/') # 重定向到首页
    else:
        return render(request, 'error.html', {'message': '用户名或密码不正确'}) # 跳转错误页面
```

错误页面 **error.html** ：

```html
{% extends 'base.html'%} <!-- 声明引用模板 -->
{% load static %}

{% block title %}
    我的网站|错误
{% endblock %}

{% block nav_home_active %}
active
{% endblock %}

{% block nav_blog_active %}
{% endblock %}

{% block content %}
    {{ message }}
{% endblock %}
```

此时运行代码，提交表单时会出现报错：

![16-03](https://img-blog.csdnimg.cn/20210712223826804.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NDMzODc4MA==,size_16,color_FFFFFF,t_70#pic_center)


这是django自带的防止跨站攻击的验证

只需要在表单提交部分添加 `{% csrf_token %}` 即可：

```html
<form action="{% url 'login' %}" method="POST">
    {% csrf_token %}
   <input type="text" name="username">
    <input type="password" name="password">
    <input type="submit" value="登录">
</form>
```

![16-04](https://img-blog.csdnimg.cn/20210712223843445.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NDMzODc4MA==,size_16,color_FFFFFF,t_70#pic_center)