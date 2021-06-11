# 03--Django笔记--模板嵌套

## 一、常用的模板标签

|   作用   |          标签           |
| :------: | :---------------------: |
|   循环   |           for           |
|   条件   | if、ifequal、ifnotequal |
|   链接   |           url           |
| 模板嵌套 | block、extends、include |
|   注释   |          {# #}          |

## 二、模板嵌套

观察几个html页面，可以发现前几次的html的大致框架都是一致的

为了方便编写，减少代码量，可以使用模板的方式，把框架部分的代码做成模板进行套用

在模板和内容的html中分别写上`{% block 代码块名称 %}{% endblock %}`，模板的部分会被继承到内容html中

在mysite/blog/templates中新建一个模板html文件 **base.html**

```html
<!DOCTYPE html>
<html lang="zh-cn">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}{% endblock %}</title> <!-- 使用block和endblock作为嵌套的代码块开始结束标志, block后面的title是代码块名称 -->
</head>
<body>
    <div>
        <a href="{% url 'home' %}">
            <h1>我的博客网站</h1>
        </a>
    </div>
    <hr>
    {% block content %}{% endblock %} <!-- 内容代码块 -->
</body>
</html>
```

然后对其他html页面进行拓展：

`{% extends 'base.html'%}` 必须写在文件最前端，声明是继承于哪个模板

**blog_detail.html**

```html
<!-- blog_detail.html -->
{% extends 'base.html'%} <!-- 声明引用模板 -->

{% block title %}
    {{ blog.title }} <!-- 这里的blog是从views.py中传入的内容 -->
{% endblock %}

{% block content %}
    <h3>{{ blog.title }}</h3>
    <p>作者：{{ blog.author }}</p>
    <p>修改时间：{{ blog.last_updated_time|date:"Y-m-d G:i:s" }}</p>
    <p>博客类型：
        <a href="{% url 'blogs_with_type' blog.blog_type.pk %}">
            {{ blog.blog_type }}
        </a>
    </p>
    <p>{{ blog.content }}</p> <!-- 其中冒号后面的内容表示显示字符长度 -->
{% endblock %}
```

**blog_list.html**

```html
{% extends 'base.html'%} <!-- 声明引用模板 -->

{% block title %}
    我的网站
{% endblock %}

{% block content %}
    <p>共有{{ blogs|length }}篇博客</p> <!-- 过滤器 -->
    {% for blog in blogs %} <!-- 这里的blog是从views.py中传入的内容 -->
        <a href="{% url 'blog_detail' blog.pk %}">
            <h3>{{ blog.title }}</h3>
        </a>
        <p>作者：{{ blog.author }}</p>
        <p>修改时间：{{ blog.last_updated_time|date:"Y-m-d G:i:s" }}</p>
        <p>博客类型：{{ blog.blog_type }}</p>
        <p>{{ blog.content|truncatechars:30 }}</p> <!-- 其中冒号后面的内容表示显示字符长度 -->
        {% empty %} <!-- 如果为空则执行下面代码 -->
        <p>--暂无博客，敬请期待--</p>
    {% endfor %}
{% endblock %}
```

**blogs_with_type.html**

```html
{% extends 'base.html'%} <!-- 声明引用模板 -->

{% block title %}
    {{ blog_type.type_name }}
{% endblock %}

{% block content %}
<div>
    <a href="{% url 'blogs_with_type' blog_type.pk %}"> <!--  此处的'home'是url的name为home的链接 -->
        <h2>博客分类：{{ blog_type.type_name }}</h2>
    </a>
</div>
<hr>
<p>共有{{ blogs|length }}篇博客</p> <!-- 过滤器 -->
    {% for blog in blogs %} <!-- 这里的blog是从views.py中传入的内容 -->
        <a href="{% url 'blog_detail' blog.pk %}">
            <h3>{{ blog.title }}</h3>
        </a>
        <p>作者：{{ blog.author }}</p>
        <p>修改时间：{{ blog.last_updated_time|date:"Y-m-d G:i:s" }}</p>
        <p>博客类型：{{ blog.blog_type }}</p>
        <p>{{ blog.content|truncatechars:30 }}</p> <!-- 其中冒号后面的内容表示显示字符长度 -->
        {% empty %} <!-- 如果为空则执行下面代码 -->
        <p>--暂无博客，敬请期待--</p>
    {% endfor %}
{% endblock %}
```

## 三、全局模板文件夹

公共的模板更适合被放在一个公共的地方，这样可以方便被全局调用

全局模板文件夹需要在 **/mysite/mysite/settings.py** 中定义

先在 **/mysite/mysite/** 文件夹下创建公共templates文件夹

![03-01](https://img-blog.csdnimg.cn/20210611183610403.png#pic_center)


然后修改 **/mysite/mysite/settings.py** 中的内容

![03-02](https://img-blog.csdnimg.cn/20210611183624882.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NDMzODc4MA==,size_16,color_FFFFFF,t_70#pic_center)


然后将 **base.html** 移动到这个文件夹中即可

现在的项目目录如下：

```bash
(study) root@***:~/Program/Django/study# tree mysite
mysite
├── blog
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   └── __init__.py
│   ├── models.py
│   ├── templates
│   │   ├── blog_detail.html
│   │   ├── blog_list.html
│   │   └── blogs_with_type.html
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── db.sqlite3
├── manage.py
├── mysite
│   ├── asgi.py
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── requirement.txt
└── templates
    └── base.html

5 directories, 21 files
```