# from mysite.blog.models import Blog
from django.core import paginator
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator # 引入分页器
from .models import Blog, BlogType
# 渲染模板文件
# Create your views here.

def blog_list(request): # 博客列表html界面的渲染
    blogs_all_list = Blog.objects.all() # 全部博客列表
    paginator = Paginator(blogs_all_list, 10) # 分页，每10篇分一页

    page_num = request.GET.get('page', 1) # request.GET得到get请求中的内容; 此处查看get请求中有没有page这个属性，没有则为1
    page_of_blogs = paginator.get_page(page_num)

    context = {} # context字典为传入html渲染的内容
    # context['blogs'] = page_of_blogs.object_list() # 获取分页中的博客列表
    context['page_of_blogs'] = page_of_blogs
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