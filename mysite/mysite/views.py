from django.shortcuts import render
from read_statistics.utils import get_seven_days_read_data, get_today_hot_data, get_yesterday_hot_data # , get_7_days_hot_data
from django.contrib.contenttypes.models import ContentType
from blog.models import Blog
import datetime
from django.core.cache import cache
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