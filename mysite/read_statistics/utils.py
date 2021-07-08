from django.contrib.contenttypes.models import ContentType
from .models import ReadNum

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
            if ReadNum.objects.filter(content_type = ct, object_id = obj.pk).count(): # 如果存在阅读记录，加1
                readnum = ReadNum.objects.get(content_type = ct, object_id = obj.pk)
            else: # 如果不存在阅读记录
                readnum = ReadNum(content_type = ct, object_id = obj.pk) # 创建阅读记录
            readnum.read_num += 1 # 阅读数量加1
            readnum.save()
    return key