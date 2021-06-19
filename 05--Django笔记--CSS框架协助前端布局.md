# 05--Django笔记--CSS框架协助前端布局

## 一、开始

打开[Bootstrap官网](https://v3.bootcss.com/)，下载Bootstrap

将下载好的文件放入静态文件文件夹，现在的文件目录如下：

```bash
root@***:~/Program/Django/study# tree mysite
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
│   ├── views.py
│   └── wsgi.py
├── requirement.txt
├── static
│   ├── bootstrap-3.4.1
│   │   ├── css
│   │   │   ├── bootstrap.css
│   │   │   ├── bootstrap.css.map
│   │   │   ├── bootstrap.min.css
│   │   │   ├── bootstrap.min.css.map
│   │   │   ├── bootstrap-theme.css
│   │   │   ├── bootstrap-theme.css.map
│   │   │   ├── bootstrap-theme.min.css
│   │   │   └── bootstrap-theme.min.css.map
│   │   ├── fonts
│   │   │   ├── glyphicons-halflings-regular.eot
│   │   │   ├── glyphicons-halflings-regular.svg
│   │   │   ├── glyphicons-halflings-regular.ttf
│   │   │   ├── glyphicons-halflings-regular.woff
│   │   │   └── glyphicons-halflings-regular.woff2
│   │   └── js
│   │       ├── bootstrap.js
│   │       ├── bootstrap.min.js
│   │       └── npm.js
│   ├── css
│   │   ├── base.css
│   │   └── home.css
│   └── js
└── templates
    ├── base.html
    └── home.html

12 directories, 41 files
```

然后再 **base.html** 文件中引用：

![05-01](https://img-blog.csdnimg.cn/20210619215525332.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NDMzODc4MA==,size_16,color_FFFFFF,t_70#pic_center)


## 二、导航栏布局

根据 **bootstrap** 官网的文档对[导航栏的介绍](https://v3.bootcss.com/components/#navbar)

```css
<div class="navbar navbar-default" role="navigation">
        <div class="container-fluid">
            <div class="navbar-header">
                <a class="navbar-brand" href="{% url 'home' %}">
                    我的博客网站
                </a>
            </div>
            <ul class="nav navbar-nav">
                <li><a href="{% url 'home' %}">首页</a></li>
                <li><a href="/blog">博客</a></li>
            </ul>
        </div>
    </div>
```

可以把导航栏部署成下面这个样子：

![05-02](https://img-blog.csdnimg.cn/20210619215540664.png#pic_center)


但是这样的布局在手机这样的小屏幕设备会堆叠。

`<button class="navbar-toggle collapsed"></button>` 中的collapsed的意思是，当设备屏幕较小，才会显示

`data-target="#navbar-collapse"` 表示会根据屏幕缩小的元素目标，“#”表示根据 **id** 寻找目标

`class="navbar-fixed-top"` 表示navbar会在顶部固定

即：

```css
<div class="navbar navbar-default navbar-fixed-top" role="navigation">
        <div class="container-fluid">
            <div class="navbar-header">
                <a class="navbar-brand" href="{% url 'home' %}">
                    我的博客网站
                </a>
                <button class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar-collapse">
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>
            </div>
            <div id="navbar-collapse" class="collapse navbar-collapse">
                <ul class="nav navbar-nav">
                    <li class="{% block nav_home_active %}{% endblock %}">
                        <a href="{% url 'home' %}">首页</a>
                    </li>
                    <li class="{% block nav_blog_active %}{% endblock %}">
                        <a href="/blog">博客</a>
                    </li>
                </ul>
            </div>
        </div>
    </div>
```



![05-03](https://img-blog.csdnimg.cn/20210619215554790.png#pic_center)
