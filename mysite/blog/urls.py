from django.urls import path
from django.urls import path
from . import views # 引入模板渲染的函数

urlpatterns = [
    # http://localhost:8000/blog/
    path('', views.blog_list, name = 'blog_list'), # 设置首页
    path('<int:blog_pk>', views.blog_detail, name = 'blog_detail'),
    path('type/<int:blogs_type_pk>', views.blogs_with_type, name = 'blogs_with_type'),
    path('date/<int:year>/<int:month>', views.blogs_with_date, name = 'blogs_with_date')
]