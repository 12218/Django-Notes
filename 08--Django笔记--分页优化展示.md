# 08--Django笔记--分页优化展示

上一次做出了分页效果，但是分页存在问题

1. 当分页过多，下方的页码导航栏长度过长
2. 没有页码高亮，不知道当前处于的页面

## 一、当前页码高亮

先判断当前页面，然后把当前页面设置为 **active** 

```html
{% if page_num == page_of_blogs.number %} <!-- 判断页码如果是当前页，则设置为高亮状态 -->
	<li class="active"><a href="?page={{ page_num }}">{{ page_num }}</a></li>
{% else %}
	<li><a href="?page={{ page_num }}">{{ page_num }}</a></li>
{% endif %}
```

## 二、缩减分页导航栏

修改传入 **blog_list.html** 的分页，保证传入的页面仅限于当前页面及前两页、后两页，和首页、尾页：

```python
# mysite/blog/views.py
def blog_list(request): # 博客列表html界面的渲染
    ...
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

    ...
    context['page_range'] = page_range
    ...
    return render(request, 'blog_list.html', context)
```

修改 **blog_list.html** 中页码部分：

```html
{% for page_num in page_range %} <!-- 修改后要在page_range中循环 -->
	{% if page_num == page_of_blogs.number %} <!-- 判断页码如果是当前页，则设置为高亮状态 -->
		<li class="active"><a href="?page={{ page_num }}">{{ page_num }}</a></li>
	{% else %}
		{% if page_num == '...' %} <!-- 让省略号不可被点击 -->
			<li><span>{{ page_num }}</span></li>
		{% else %}
			<li><a href="?page={{ page_num }}">{{ page_num }}</a></li>
		{% endif %}
	{% endif %}
{% endfor %}
```

![08-01](https://img-blog.csdnimg.cn/20210627222826973.png#pic_center)


由于 **blogs_with_type.html** 是继承于 **blog_list.html** 文件

所以 **views.py** 中的 **blogs_with_type** 函数需要修改

```python
def blogs_with_type(request, blogs_type_pk):
    context = {}
    blog_type = get_object_or_404(BlogType, pk = blogs_type_pk)

    blogs_all_list = Blog.objects.filter(blog_type = blog_type)
    paginator = Paginator(blogs_all_list, 10) # 分页，每10篇分一页

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


    context['page_of_blogs'] = page_of_blogs
    context['blog_types'] = BlogType.objects.all()
    context['blog_type'] = blog_type
    context['page_range'] = page_range
    return render(request, 'blogs_with_type.html', context)
```

## 三、将每页博客数量变量设为全局变量

公共全局设置可以放在 **settings.py** 文件中，进行统一管理

调用方法：

```python
from django.conf import settings
settings.xxx
```

具体操作如下：

现在 **settings.py** 文件中设置变量：

![08-02](https://img-blog.csdnimg.cn/20210627222840776.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NDMzODc4MA==,size_16,color_FFFFFF,t_70#pic_center)


然后修改 **views.py** ：

```python
paginator = Paginator(blogs_all_list, settings.EACH_PAGE_BLOGS_NUMBER) # 分页，每10篇分一页
```
