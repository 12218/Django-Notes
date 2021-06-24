# 07--Django笔记--分页和shell命令行模式

## shell 命令行模式

### 一、shell添加博客

1. `python3 manage.py shell` 进入shell命令行

```bash
(study) root@***:~/Program/Django/study/mysite# python3 manage.py shell
Python 3.8.5 (default, May 27 2021, 13:30:53) 
[GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> from blog.models import Blog
>>> dir()
['Blog', '__builtins__']
>>> Blog.objects.all()
<QuerySet [<Blog: <Blog: Django笔记01>>, <Blog: <Blog: python>>, <Blog: <Blog: 长内容博客>>]>
>>> Blog.objects.all().count()
3
>>>
```

2. 添加博客

```bash
(study) root@***:~/Program/Django/study/mysite# python3 manage.py shell
Python 3.8.5 (default, May 27 2021, 13:30:53) 
[GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> from blog.models import Blog, BlogType
>>> from django.contrib.auth.models import User
>>> blog = Blog()
>>> blog.title = "Django shell命令行"
>>> blog.content = "Django shell命令行的文章内容"
>>> blog.blog_type = BlogType.objects.all()[0]
>>> blog.author = User.objects.all()[0]
>>> blog.save()
>>> Blog.objects.all()
<QuerySet [<Blog: <Blog: Django笔记01>>, <Blog: <Blog: python>>, <Blog: <Blog: 长内容博客>>, <Blog: <Blog: Django shell命令行>>]>
>>>
```

![07-01](https://img-blog.csdnimg.cn/20210624223128677.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NDMzODc4MA==,size_16,color_FFFFFF,t_70#pic_center)


添加成功

### 二、多博客添加范例：

```bash
>>> for i in range(1, 31):
...     blog = Blog()
...     blog.title = "for %s" % i
...     blog.content = "这是第%s篇博客的内容" % i
...     blog.blog_type = BlogType.objects.all()[1]
...     blog.author = User.objects.all()[0]
...     blog.save()
... 
>>> Blog.objects.all().count()
34
>>>
```

## 博客分页

### 一、分页

Django中有自带的分页器

首先对文章排序进行规定：

![07-02](https://img-blog.csdnimg.cn/20210624223152820.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NDMzODc4MA==,size_16,color_FFFFFF,t_70#pic_center)


然后对数据库进行迁移，使之生效。

![07-03](https://img-blog.csdnimg.cn/20210624223213439.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NDMzODc4MA==,size_16,color_FFFFFF,t_70#pic_center)


博客会默认按照时间排序。

```bash
(study) root@***:~/Program/Django/study/mysite# python3 manage.py shell
Python 3.8.5 (default, May 27 2021, 13:30:53) 
[GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> from blog.models import Blog, BlogType
>>> from django.core.paginator import Paginator
>>> blogs = Blog.objects.all()
>>> paginator = Paginator(blogs, 10)
>>> dir(paginator)
['ELLIPSIS', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_check_object_list_is_ordered', '_get_page', 'allow_empty_first_page', 'count', 'get_elided_page_range', 'get_page', 'num_pages', 'object_list', 'orphans', 'page', 'page_range', 'per_page', 'validate_number']
>>> page1 = paginator.page(1)
>>> dir(page1)
['__abstractmethods__', '__class__', '__contains__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__reversed__', '__setattr__', '__sizeof__', '__slots__', '__str__', '__subclasshook__', '__weakref__', '_abc_impl', 'count', 'end_index', 'has_next', 'has_other_pages', 'has_previous', 'index', 'next_page_number', 'number', 'object_list', 'paginator', 'previous_page_number', 'start_index']
>>>
```

分页分好之后，进行代码规划。

前端发送请求，打开具体分页内容；后端处理请求，返回分页内容响应。

### 二、设计请求

在blog应用中的 **view.py** 中设计请求

```python
...
from django.core.paginator import Paginator # 引入分页器
...

def blog_list(request): # 博客列表html界面的渲染
    blogs_all_list = Blog.objects.all() # 全部博客列表
    paginator = Paginator(blogs_all_list, 10) # 分页，每10篇分一页

    page_num = request.GET.get('page', 1) # request.GET得到get请求中的内容; 此处查看get请求中有没有page这个属性，没有则为1
    page_of_blogs = paginator.get_page(page_num)

    context = {} # context字典为传入html渲染的内容
    # context['blogs'] = page_of_blogs.object_list() # 获取分页中的博客列表
    context['page_of_blogs'] = page_of_blogs
    context['blog_types'] = BlogType.objects.all()
    # context['blogs_count'] = Blog.objects.all().count() # 获取博客数量
    return render(request, 'blog_list.html', context)
```

然后对 **blog_list.html** 中进行修改

```html
...
<div class="panel-heading">
    {% block block_list_title %}博客列表——共有{{ page_of_blogs.paginator.count|length }}篇博客{% endblock %}
</div>
...
{% for blog in page_of_blogs.object_list %}
```

![07-04](https://img-blog.csdnimg.cn/20210624223238735.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NDMzODc4MA==,size_16,color_FFFFFF,t_70#pic_center)


### 三、设置html中的页码

页码可以使用bootstrap进行美化，参照[官网](https://v3.bootcss.com/components/#pagination)

```html
<div aria-label="Page navigation"> <!-- 页码设置 -->
    <ul class="pagination">
        <li>
            {% if page_of_blogs.has_previous %}
            <a href="?page={{ page_of_blogs.previous_page_number }}" aria-label="Previous">
                <span aria-hidden="true">&laquo;</span>
            </a>
            {% else %}
            <span aria-hidden="true">&laquo;</span>
            {% endif %}
        </li>
        {% for page_num in page_of_blogs.paginator.page_range %}
        <li><a href="?page={{ page_num }}">{{ page_num }}</a></li>
        {% endfor %}
        <li>
            {% if page_of_blogs.has_next %}
            <a href="?page={{ page_of_blogs.next_page_number }}" aria-label="Next">
                <span aria-hidden="true">&raquo;</span>
            </a>
            {% else %}
            <span aria-hidden="true">&raquo;</span>
            {% endif %}
        </li>
    </ul>
</div>
```
