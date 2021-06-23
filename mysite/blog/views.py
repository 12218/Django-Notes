# from mysite.blog.models import Blog
from django.shortcuts import render, get_object_or_404
from .models import Blog, BlogType
# 渲染模板文件
# Create your views here.

def blog_list(request): # 博客列表html界面的渲染
    context = {} # context字典为传入html渲染的内容
    context['blogs'] = Blog.objects.all() # Blog.objects.all()为选择数据库中所有博客
    context['blog_types'] = BlogType.objects.all()
    # context['blogs_count'] = Blog.objects.all().count() # 获取博客数量
    return render(request, 'blog_list.html', context)

def blog_detail(request, blog_pk): # 博客细节html界面的渲染；其中blog_pk参数为博客编号(pk意思为外键)
    context = {} # context字典为传入html渲染的内容
    context['blog'] = get_object_or_404(Blog, id = blog_pk) # get_object_or_404()在无法取到object的时候返回404界面
    return render(request, 'blog_detail.html', context)

def blogs_with_type(request, blogs_type_pk):
    context = {}
    blog_type = get_object_or_404(BlogType, pk = blogs_type_pk)
    context['blogs'] = Blog.objects.filter(blog_type = blog_type) # 筛选函数
    context['blog_types'] = BlogType.objects.all()
    context['blog_type'] = blog_type
    return render(request, 'blogs_with_type.html', context)