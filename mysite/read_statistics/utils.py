import datetime
from django.contrib.contenttypes.models import ContentType
from .models import ReadNum, ReadDetail
from django.db.models import Sum
from django.utils import timezone

def read_statistics_once_read(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    key = "%s_%s_read" % (ct.model, obj.pk)

    if not request.COOKIES.get(key):
            # blog.readed_num += 1 # 阅读量每次加一
            # blog.save() # 博客保存
            '''if ReadNum.objects.filter(blog = blog).count(): # 如果存在阅读记录，加1
                readnum = ReadNum.objects.get(blog = blog)
            else: # 如果不存在阅读记录
                readnum = ReadNum() # 创建阅读记录
                readnum.blog = blog
            readnum.read_num += 1 # 阅读数量加1
            readnum.save()'''

            # 某博客阅读总数+1
            readnum, created = ReadNum.objects.get_or_create(content_type = ct, object_id = obj.pk)
            readnum.read_num += 1 # 阅读数量加1
            readnum.save()

            # 某博客当天阅读数量+1
            nowdate = timezone.now()
            readDetail, created = ReadDetail.objects.get_or_create(content_type = ct, object_id = obj.pk, date = nowdate)
            readDetail.read_num += 1
            readDetail.save()
    return key

# 获取过去7天每天阅读数量
def get_seven_days_read_data(content_type):
    today = timezone.now().date() # 取出今天的日期
    dates = []
    read_nums = [] # 阅读数量数组
    
    for i in range(7, 0, -1):
        date = today - datetime.timedelta(days = i)
        read_details = ReadDetail.objects.filter(content_type = content_type, date = date)
        result = read_details.aggregate(read_num_sum = Sum('read_num')) # 聚合函数，统计确定日期下所有博客的所有阅读量，统计取名为read_num_sum
        dates.append(date.strftime('%m/%d'))
        read_nums.append(result['read_num_sum'] or 0) # 将result中read_num_sum的结果加入到阅读数量数组，如果不存在，则添加0
    return dates, read_nums

# 获取今天热门阅读博客数据
def get_today_hot_data(content_type):
    today = timezone.now().date() # 取出今天的日期
    read_details = ReadDetail.objects.filter(content_type = content_type, date = today).order_by('-read_num') # 由大到小按照read_num排序
    return read_details[:7] # 限制取前7条数据

# 获取昨天热门阅读博客数据
def get_yesterday_hot_data(content_type):
    today = timezone.now().date() # 取出今天的日期
    yesterday = today - datetime.timedelta(days = 1)
    read_details = ReadDetail.objects.filter(content_type = content_type, date = yesterday).order_by('-read_num') # 由大到小按照read_num排序
    return read_details[:7] # 限制取前7条数据

# # 获取过去7天热门阅读博客数据
# def get_7_days_hot_data(content_type):
#     today = timezone.now().date() # 取出今天的日期
#     seven_date = today - datetime.timedelta(days = 7)
#     read_details = ReadDetail.objects\
#         .filter(content_type = content_type, date__lt = today, date__gte = seven_date)\
#         .values('content_type', 'object_id')\
#         .annotate(read_num_sum = Sum('read_num'))\
#         .order_by('-read_num_sum')
#     return read_details[:7]