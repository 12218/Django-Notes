from django.shortcuts import render
from read_statistics.utils import get_seven_days_read_data
from django.contrib.contenttypes.models import ContentType
from blog.models import Blog

def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read_data(blog_content_type) # 获取过去7天阅读数量数组

    context = {}
    context['dates'] = dates
    context['read_nums'] = read_nums # 将阅读数组传入前端页面
    return render(request, 'home.html', context)