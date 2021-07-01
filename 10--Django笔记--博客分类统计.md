# 10--Django笔记--博客分类统计

## 一、方式一

在 **views.py** 文件中的 **get_blog_list_common_date** 方法中设置一个列表，传进html

**blog_type_list** 包含两个属性，一个是博客名，另外一个是博客数量

```python
def get_blog_list_common_date(request, blogs_all_list):
    ...
    # 获取各个博客分类中的博客数量
    blog_types = BlogType.objects.all()
    blog_type_list = []
    for blog_type in blog_types:
        blog_type.blog_count = Blog.objects.filter(blog_type = blog_type).count()
        blog_type_list.append(blog_type)
    ...
    context['blog_types'] = blog_type_list
    ...
```

再对 **blog_list.html** 文件进行修改：

```html
<ul class="blog-types">
    {% for blog_type in blog_types %}
    <li>
        <a href="{% url 'blogs_with_type' blog_type.pk %}">
            {{ blog_type.type_name }} ({{ blog_type.blog_count }})
        </a>
    </li>
    {% empty %}
    <li>没有分类</li>
    {% endfor %}
</ul>
```

效果如下：

![10-01](https://img-blog.csdnimg.cn/20210701215522289.png#pic_center)


## 二、方式二

Django还为用户准备了一个工具：**annotate**

先在 **models.py** 中设置 **blog_type** 的名称：

```python
blog_type = models.ForeignKey(BlogType, on_delete = models.DO_NOTHING, related_name = 'blog_blog') # BlogType是自己设置的博客分类
```

这时就可以在 **views.py** 文件中直接调用“blog_blog”：

```python
def get_blog_list_common_date(request, blogs_all_list):
    ...
    # 获取各个博客分类中的博客数量
    blog_type_list = BlogType.objects.annotate(blog_count = Count('blog_blog'))
    ...
    context['blog_types'] = blog_type_list
    ...
```