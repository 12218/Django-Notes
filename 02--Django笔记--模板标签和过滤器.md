# 02--Django笔记--模板标签和过滤器

## 一、搭建渲染模板

渲染模板的文件位于应用文件夹中的 **views.py** 文件中

![02-01](https://img-blog.csdnimg.cn/20210610225451218.png#pic_center)


渲染模板即为请求后返回的html文件的渲染

之后修改 **views.py** 创建渲染函数

```python
# from mysite.blog.models import Blog
from django.shortcuts import render, get_object_or_404
from .models import Blog, BlogType
# 渲染模板文件
# Create your views here.

def blog_list(request): # 博客列表html界面的渲染
    context = {} # context字典为传入html渲染的内容
    context['blogs'] = Blog.objects.all() # Blog.objects.all()为选择数据库中所有博客
    return render(request, 'blog_list.html', context)

def blog_detail(request, blog_pk): # 博客细节html界面的渲染；其中blog_pk参数为博客编号(pk意思为外键)
    context = {} # context字典为传入html渲染的内容
    context['blog'] = get_object_or_404(Blog, id = blog_pk) # get_object_or_404()在无法取到object的时候返回404界面
    return render(request, 'blog_detail.html', context)
```

但是此时并没有用于渲染的 **blog_list.html** 和 **blog_detail.html** 文件

需要在应用内创建 **templates** 文件夹后，在文件夹下加入这两个文件

```html
<!-- blog_list.html --> 
<!DOCTYPE html>
<html lang="zh-cn">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>我的网站</title>
</head>
<body>
    {% for blog in blogs %} <!-- 这里的blog是从views.py中传入的内容 -->
        <h3>{{ blog.title }}</h3>
        <p>{{ blog.content }}</p>
    {% endfor %}
</body>
</html>
```

```html
<!-- blog_detail.html -->
<!DOCTYPE html>
<html lang="zh-cn">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ blog.title }}</title><!-- 这里的blog是从views.py中传入的内容 -->
</head>
<body>
    <h3>{{ blog.title }}</h3>
    <p>{{ blog.content }}</p>
</body>
</html>
```

## 二、路由搭建

创建完模板渲染之后，还不能立刻访问，必须要先设置路由

需要在应用文件夹下创建 **urls.py** 加入路由

```python
# urls.py
from django.urls import path
from django.urls import path
from . import views # 引入模板渲染的函数

urlpatterns = [
    # http://localhost:8000/blog/1
    path('<int:blog_pk>', views.blog_detail, name = 'blog_detail'),
]
```

然后再在项目文件夹 **urls.py** 中加入路由

![02-02](https://img-blog.csdnimg.cn/2021061022551226.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NDMzODc4MA==,size_16,color_FFFFFF,t_70#pic_center)


当路由全部设置完毕后，即可运行代码

效果如下：

![02-03](https://img-blog.csdnimg.cn/20210610225526659.png#pic_center)


![02-04](https://img-blog.csdnimg.cn/20210610225543293.png#pic_center)


## 三、html优化

### 1. 链接设置

在html中设置可以跳转的链接可以使用如下方式：

![02-05](https://img-blog.csdnimg.cn/20210610225556500.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NDMzODc4MA==,size_16,color_FFFFFF,t_70#pic_center)


其中在 **urls.py** 中设置的url的名称可以直接使用。

### 2. 过滤器

#### 博客长度问题

**{{ blogs|length }}** 可以获取博客长度

```html
<p>共有{{ blogs|length }}篇博客</p> <!-- 过滤器 -->
```

效果如下：

![02-06](https://img-blog.csdnimg.cn/20210610225613314.png#pic_center)


#### 解决长博客显示问题

如果博客是长博客，也会将所有内容显示到博客列表：

![02-07](https://img-blog.csdnimg.cn/20210610225635864.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NDMzODc4MA==,size_16,color_FFFFFF,t_70#pic_center)


可以使用过滤器修改博客显示长度：

```html
<p>{{ blog.content|truncatechars:30 }}</p> <!-- 其中冒号后面的内容表示显示字符长度 -->
<!-- 或者使用truncatewords:30，表示显示前30个单词 -->
```

效果如下：

![02-08](https://img-blog.csdnimg.cn/20210610225649946.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NDMzODc4MA==,size_16,color_FFFFFF,t_70#pic_center)


#### 时间显示问题

可以使用过滤器对时间进行格式化：

```html
<p>修改时间：{{ blog.last_updated_time|date:"Y-m-d G:i:s" }}</p>
<!-- 修改时间：2021-06-09 22:34:00 -->
```



#### 时间显示问题

可以使用过滤器对时间进行格式化：

```html
<p>修改时间：{{ blog.last_updated_time|date:"Y-m-d G:i:s" }}</p>
<!-- 修改时间：2021-06-09 22:34:00 -->
```

