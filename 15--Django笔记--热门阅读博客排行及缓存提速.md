# 15--Django笔记--热门阅读博客排行及缓存提速

## 一、添加方法

在 **utils.py** 中增加返回今天阅读数量的函数：

```python
# 获取今天热门阅读博客数据
def get_today_hot_data(content_type):
    today = timezone.now().date() # 取出今天的日期
    read_details = ReadDetail.objects.filter(content_type = content_type, date = today).order_by('-read_num') # 由大到小按照read_num排序
    return read_details[:7] # 限制取前7条数据
```

然后在 **mysite/mysite/views.py** 中调用，并传入前端页面：

```python
from django.shortcuts import render
from read_statistics.utils import get_seven_days_read_data, get_today_hot_data
from django.contrib.contenttypes.models import ContentType
from blog.models import Blog

def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read_data(blog_content_type) # 获取过去7天阅读数量数组

    today_hot_data = get_today_hot_data(blog_content_type) # 获取今日阅读数据

    context = {}
    context['dates'] = dates
    context['read_nums'] = read_nums # 将阅读数组传入前端页面
    context['today_hot_data'] = today_hot_data
    return render(request, 'home.html', context)
```

前端页面：

```python
<!-- 今天热门博客 -->
<h3>今日热门博客</h3>
    <ul>
        {% for hot_data in today_hot_data %}
            <li>
                <a href="{% url 'blog_detail' hot_data.object_id %}">
                    {{ hot_data.content_object.title }}({{ hot_data.read_num }})
                </a>
            </li>            
        {% empty %}
            <li>今天暂无热门博客</li>
        {% endfor %}
    </ul>
```

![15-01](https://img-blog.csdnimg.cn/20210711223934323.png#pic_center)


过去7天博客统计：

```python
# 获取过去7天热门阅读博客数据
def get_7_days_hot_data(content_type):
    today = timezone.now().date() # 取出今天的日期
    seven_date = today - datetime.timedelta(days = 7)
    read_details = ReadDetail.objects\
        .filter(content_type = content_type, date__lt = today, date__gte = seven_date)\
        .values('content_type', 'object_id')\
        .annotate(read_num_sum = Sum('read_num'))\
        .order_by('-read_num_sum')
    return read_details[:7]
```

其中， **values** 是将筛选出来的数据按照content_type和object_id进行分组

**annotate** 是注释，把read_num的总和记为read_num_sum

为了传给前端页面，需要进行如下操作：

修改 **models.py** ：

```python
...
from read_statistics.models import ReadNumExpandMethod, ReadDetail
from django.contrib.contenttypes.fields import GenericRelation
...
# 设置每篇博客的属性
class Blog(models.Model, ReadNumExpandMethod):
...
    read_details = GenericRelation(ReadDetail)
...
```

修改 **views.py** ：

```python
from django.shortcuts import render
from read_statistics.utils import get_seven_days_read_data, get_today_hot_data, get_yesterday_hot_data, get_7_days_hot_data
from django.contrib.contenttypes.models import ContentType
from blog.models import Blog
import datetime
from django.utils import timezone
from django.db.models import Sum

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

    today_hot_data = get_today_hot_data(blog_content_type) # 获取今日阅读数据
    yesterday_hot_data = get_yesterday_hot_data(blog_content_type) # 获取昨日阅读数据
    seven_days_hot_data = get_7_days_blogs() # 过去7天的阅读数据

    context = {}
    context['dates'] = dates
    context['read_nums'] = read_nums # 将阅读数组传入前端页面
    context['today_hot_data'] = today_hot_data
    context['yesterday_hot_data'] = yesterday_hot_data
    context['seven_days_hot_data'] = seven_days_hot_data
    return render(request, 'home.html', context)
```

## 二、缓存数据

### [数据库缓存](https://docs.djangoproject.com/zh-hans/3.2/topics/cache/#database-caching)

在 **settings.py** 中添加以下代码：

```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'my_cache_table',
    }
}
```

![15-02](https://img-blog.csdnimg.cn/20210711223955430.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NDMzODc4MA==,size_16,color_FFFFFF,t_70#pic_center)


设置、访问缓存方法：

![15-03](https://img-blog.csdnimg.cn/20210711224008225.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NDMzODc4MA==,size_16,color_FFFFFF,t_70#pic_center)


**注：在使用缓存之前，需要先设置缓存表：**

```bash
python3 manage.py createcachetable
```

使用缓存：

```python
...
from django.core.cache import cache
...

def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read_data(blog_content_type) # 获取过去7天阅读数量数组

    # 获取7天热门博客的缓存数据
    hot_blogs_for_7_days = cache.get('hot_blogs_for_7_days')
    if hot_blogs_for_7_days is None:
        hot_blogs_for_7_days = get_7_days_blogs()
        cache.set('hot_blogs_for_7_days', hot_blogs_for_7_days, 3600)
    else:
        print('use cache')

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
```

![15-04](https://img-blog.csdnimg.cn/20210711224044229.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NDMzODc4MA==,size_16,color_FFFFFF,t_70#pic_center)

