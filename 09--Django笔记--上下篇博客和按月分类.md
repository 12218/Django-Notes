# 09--Django笔记--上下篇博客和按月分类

## 一、添加上下篇博客

### filter筛选条件

Django中的filter函数已经集成了很多中查找类型

![09-01](https://img-blog.csdnimg.cn/2021063022570530.PNG?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NDMzODc4MA==,size_16,color_FFFFFF,t_70#pic_center)


添加上下篇博客的跳转可以使用filter进行选取

```python
def blog_detail(request, blog_pk): # 博客细节html界面的渲染；其中blog_pk参数为博客编号(pk意思为外键)
    context = {} # context字典为传入html渲染的内容
    blog = get_object_or_404(Blog, id = blog_pk) # get_object_or_404()在无法取到object的时候返回404界面
    context['previous_blog'] = Blog.objects.filter(create_time__gt=blog.create_time).last() # 寻找比当前博客创建时间数值大的最后一篇博客
    context['next_blog'] = Blog.objects.filter(create_time__lt=blog.create_time).first() # 寻找比当前博客创建时间数值小的第一篇博客
    context['blog'] = blog
    return render(request, 'blog_detail.html', context)
```

然后再在 **blog_detail.html** 中进行元素添加：

```html
<div class="blog-more">
    <p>上一篇：
        {% if previous_blog %}
        	<a href="{% url 'blog_detail' previous_blog.pk %}">
                {{ previous_blog.title }}
        	</a>
        {% else %}
        	没有了
        {% endif %}
    </p>
    <p>
        下一篇：
        {% if next_blog %}
        	<a href="{% url 'blog_detail' next_blog.pk %}">
                {{ next_blog.title }}
        	</a>
        {% else %}
        	没有了
        {% endif %}
    </p>
</div>
```

### exclude排除条件

exclude用法和filter用法一致，在结果上，是filter结果的取反

## 二、按月分类

先设计好按月分类的url：

```python
urlpatterns = [
    path('', views.blog_list, name = 'blog_list'), # 设置首页
    path('<int:blog_pk>', views.blog_detail, name = 'blog_detail'),
    path('type/<int:blogs_type_pk>', views.blogs_with_type, name = 'blogs_with_type'),
    path('date/<int:year>/<int:month>', views.blogs_with_date, name = 'blogs_with_date')
]
```

然后设置 **views.py** 中的方法：

```python
def blog_list(request): # 博客列表html界面的渲染
    ...
    context['blog_dates'] = Blog.objects.dates('create_time', 'month', order = 'ASC') # 传入博客日期
```

上面的这一行代码是筛选出来博客的日期

之后再在html页面中展现：

```html
<div class="panel panel-primary">
    <div class="panel-heading">日期分类</div>
    <div class="panel-body">
        <ul class="blog-types">
            {% for blog_date in blog_dates %}
            <li>
                <a href="{% url 'blogs_with_date' blog_date.year blog_date.month %}">
                    {{ blog_date|date:"Y年m月" }}
                </a>
            </li>
            {% endfor %}
        </ul>
    </div>
</div>
```

然后处理返回的请求：

```python
def blogs_with_date(request, year, month):
    context = {}

    blogs_all_list = Blog.objects.filter(create_time__year = year, create_time__month = month)
    paginator = Paginator(blogs_all_list, settings.EACH_PAGE_BLOGS_NUMBER) # 分页，每10篇分一页

    page_num = request.GET.get('page', 1) # request.GET得到get请求中的内容; 此处查看get请求中有没有page这个属性，没有则为1
    page_of_blogs = paginator.get_page(page_num)
    current_page_num = page_of_blogs.number # 获取当前页码
    # page_range = [current_page_num - 2, current_page_num - 1, current_page_num, current_page_num + 1, current_page_num + 2] # 会出现页码小于1或者大于最大页码的问题
    # 获取当前页码及前后2页
    page_range = list(range(max(current_page_num - 2, 1), current_page_num)) + \
        list(range(current_page_num, min(current_page_num + 2, paginator.num_pages) + 1))
    # 加上页码之间的省略号
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 保留首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)


    context['blogs_with_date'] = '%s年%s月' % (year, month)
    context['page_of_blogs'] = page_of_blogs
    context['blog_types'] = BlogType.objects.all()
    context['page_range'] = page_range
    context['blog_dates'] = Blog.objects.dates('create_time', 'month', order = 'ASC') # 传入博客日期
    return render(request, 'blogs_with_date.html', context)
```

![09-02](https://img-blog.csdnimg.cn/20210630225721288.png#pic_center)


## 三、代码简化

从之前的代码编写可以看到有很多代码存在冗余

可以编写一个列表函数进行调用，减少冗余

```python
def get_blog_list_common_date(request, blogs_all_list):
    paginator = Paginator(blogs_all_list, settings.EACH_PAGE_BLOGS_NUMBER) # 分页，每10篇分一页

    page_num = request.GET.get('page', 1) # request.GET得到get请求中的内容; 此处查看get请求中有没有page这个属性，没有则为1
    page_of_blogs = paginator.get_page(page_num)
    current_page_num = page_of_blogs.number # 获取当前页码
    # page_range = [current_page_num - 2, current_page_num - 1, current_page_num, current_page_num + 1, current_page_num + 2] # 会出现页码小于1或者大于最大页码的问题
    # 获取当前页码及前后2页
    page_range = list(range(max(current_page_num - 2, 1), current_page_num)) + \
        list(range(current_page_num, min(current_page_num + 2, paginator.num_pages) + 1))
    # 加上页码之间的省略号
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 保留首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    context = {} # context字典为传入html渲染的内容
    # context['blogs'] = page_of_blogs.object_list() # 获取分页中的博客列表
    context['page_of_blogs'] = page_of_blogs
    context['blog_types'] = BlogType.objects.all()
    context['page_range'] = page_range
    context['blog_dates'] = Blog.objects.dates('create_time', 'month', order = 'ASC') # 传入博客日期
    # context['blogs_count'] = Blog.objects.all().count() # 获取博客数量
    return context

def blog_detail(request, blog_pk): # 博客细节html界面的渲染；其中blog_pk参数为博客编号(pk意思为外键)
    context = {} # context字典为传入html渲染的内容
    blog = get_object_or_404(Blog, id = blog_pk) # get_object_or_404()在无法取到object的时候返回404界面
    context['previous_blog'] = Blog.objects.filter(create_time__gt=blog.create_time).last() # 寻找比当前博客创建时间数值大的最后一篇博客
    context['next_blog'] = Blog.objects.filter(create_time__lt=blog.create_time).first() # 寻找比当前博客创建时间数值小的第一篇博客
    context['blog'] = blog
    return render(request, 'blog_detail.html', context)

def blog_list(request): # 博客列表html界面的渲染
    blogs_all_list = Blog.objects.all() # 全部博客列表
    context = get_blog_list_common_date(request, blogs_all_list)
    return render(request, 'blog_list.html', context)

def blogs_with_type(request, blogs_type_pk):
    blog_type = get_object_or_404(BlogType, pk = blogs_type_pk)
    blogs_all_list = Blog.objects.filter(blog_type = blog_type)
    context = get_blog_list_common_date(request, blogs_all_list)
    context['blog_type'] = blog_type
    return render(request, 'blogs_with_type.html', context)

def blogs_with_date(request, year, month):
    blogs_all_list = Blog.objects.filter(create_time__year = year, create_time__month = month)
    context = get_blog_list_common_date(request, blogs_all_list)
    context['blogs_with_date'] = '%s年%s月' % (year, month)
    return render(request, 'blogs_with_date.html', context)
```

这样编写可以减少冗余的同时，达到预先目标。
