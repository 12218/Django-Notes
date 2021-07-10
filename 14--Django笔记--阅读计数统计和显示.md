# 14--Django笔记--阅读计数统计和显示

现在博客制作已经完成了阅读计数，但是还没有实现阅读的统计

## 一、阅读统计

首先在 **/mysite/read_statistics/models.py** 中添加模型：

```python
...
from django.utils import timezone
...
class ReadDetail(models.Model):
    date = models.DateField(default = timezone.now) # 默认时间设置为现在时间
    read_num = models.IntegerField(default = 0)

    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
```

然后数据库迁移，在 **admin.py** 中注册应用：

```python
from django.contrib import admin
from .models import ReadNum, ReadDetail
...
@admin.register(ReadDetail)
class ReadNumAdmin(admin.ModelAdmin): # 注册阅读量模型
    list_display = ('date', 'read_num', 'content_object')
```

打开管理员界面即可见到效果：

![14-01](https://img-blog.csdnimg.cn/20210710221703119.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NDMzODc4MA==,size_16,color_FFFFFF,t_70#pic_center)


之后，再添加阅读数量和日期之间的联系，原理和阅读量增加原理类似：

```python
...
from .models import ReadNum, ReadDetail
from django.utils import timezone

def read_statistics_once_read(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    key = "%s_%s_read" % (ct.model, obj.pk)

    if not request.COOKIES.get(key):
            ...
            nowdate = timezone.now()
            if ReadDetail.objects.filter(content_type = ct, object_id = obj.pk, date = nowdate).count(): # 如果存在记录且日期为今天，阅读量加1
                readDetail = ReadDetail.objects.get(content_type = ct, object_id = obj.pk, date = nowdate)
            else:
                readDetail = ReadDetail(content_type = ct, object_id = obj.pk, date = nowdate)
            readDetail.read_num += 1
            readDetail.save()
    return key
```

现在阅读数量会和日期建立联系：

![14-02](https://img-blog.csdnimg.cn/20210710221718679.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NDMzODc4MA==,size_16,color_FFFFFF,t_70#pic_center)


### 简化阅读量方法

django有一个自带的方法 **get_or_create** ，如果get不到博客，就直接创建

故此阅读量增加方法可以更改成这样：

```python
# 某博客阅读总数+1
readnum, created = ReadNum.objects.get_or_create(content_type = ct, object_id = obj.pk)
readnum.read_num += 1 # 阅读数量加1
readnum.save()

# 某博客当天阅读数量+1
nowdate = timezone.now()
readDetail, created = ReadDetail.objects.get_or_create(content_type = ct, object_id = obj.pk, date = nowdate)
readDetail.read_num += 1
readDetail.save()
```

也能达到同样的效果

然后在 **utils.py** 中使用数组和循环取出过去7天的阅读统计：

```python
# 获取过去7天每天阅读数量
def get_seven_days_read_data(content_type):
    today = timezone.now().date() # 取出今天的日期
    dates = []
    read_nums = [] # 阅读数量数组
    
    for i in range(7, 0, -1):
        date = today - datetime.timedelta(days = i)
        read_details = ReadDetail.objects.filter(content_type = content_type, date = date)
        result = read_details.aggregate(read_num_sum = Sum('read_num')) # 聚合函数，统计确定日期下所有博客的所有阅读量，统计取名为read_num_sum
        dates.append(date)
        read_nums.append(result['read_num_sum'] or 0) # 将result中read_num_sum的结果加入到阅读数量数组，如果不存在，则添加0
    return read_nums
```

然后在 **mysite/mysite/views.py** 中调用，并传入前端页面：

```python
from django.shortcuts import render
from read_statistics.utils import get_seven_days_read_data
from django.contrib.contenttypes.models import ContentType
from blog.models import Blog

def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    read_nums = get_seven_days_read_data(blog_content_type) # 获取过去7天阅读数量数组

    context = {}
    context['read_nums'] = read_nums # 将阅读数组传入前端页面
    return render(request, 'home.html', context)
```

## 二、显示数据图表

[highcharts官网](https://www.highcharts.com.cn/)

[入门文档](https://www.highcharts.com.cn/docs/start-helloworld)

Highcharts 最基本的运行只需要一个 JS 文件，即 highcharts.js，以使用 CDN 文件为例，对应的代码是：

```html
<script src="http://cdn.highcharts.com.cn/highcharts/highcharts.js"></script>
```

在 **home.html** 页面添加图表代码：

```html
{% block content %}
    <h3 class="home-content">欢迎访问我的网站</h3>
    <!-- 图表容器 DOM -->
    <div id="container" style="width: 600px;height:400px;"></div>
    <script>
        // 图表配置
        var options = {
            chart: {
                type: 'line'                          //指定图表的类型，默认是折线图（line）
            },
            title: {
                text: null                 // 标题
            },
            xAxis: {
                categories: {{ dates|safe }},   // x 轴分类
                tickmarkPlacement: 'on',
            },
            yAxis: {
                title: {
                    text: '阅读量'                // y 轴标题
                },
                labels: {
                    enabled: false // 去掉y轴标签
                },
                gridLineDashStyle: 'Dash', // 坐标轴虚线
            },
            series: [{                              // 数据列
                name: '阅读量',                        // 数据列名
                data: {{ read_nums }}                     // 数据
            }],
            plotOptions: { // 数据标签
                line: {
                    dataLabels: {
                        enabled: true
                    }
                }
            },
            legend: {
                enabled:false // 去掉图例
            },
            credits: {
                enabled: false // 去掉右下角highcharts图标
            },
        };
        // 图表初始化函数
        var chart = Highcharts.chart('container', options);
    </script>
{% endblock %}
```

![14-03](https://img-blog.csdnimg.cn/20210710221744107.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NDMzODc4MA==,size_16,color_FFFFFF,t_70#pic_center)

