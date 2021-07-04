# 12--Django笔记--博客阅读简单计数

## 一、修改模型

首先将博客的模型进行修改，加上属性 **readed_num** 

```python
readed_num = models.IntegerField(default = 0) # 博客阅读次数
```

然后迁移数据库使之生效

再在 **admin.py** 文件中修改，使之在admin页面显示

![12-01](https://img-blog.csdnimg.cn/20210704121928861.png#pic_center)


## 二、增加阅读量

如果要让阅读数量每次加一，可以在博客打开内容页面时，readed_num加一

```python
def blog_detail(request, blog_pk): # 博客细节html界面的渲染；其中blog_pk参数为博客编号(pk意思为外键)
    blog = get_object_or_404(Blog, id = blog_pk) # get_object_or_404()在无法取到object的时候返回404界面
    blog.readed_num += 1 # 阅读量每次加一
    blog.save() # 博客保存
	...
```

之后再 **blog_detail.html** 中显示

```html
<li>阅读量：{{ blog.readed_num }}</li>
```

## 三、阅读量划分

但是现在显示的情况是，只要有人打开这个页面，或者同一个人一直刷新页面，阅读量也会上涨

可以使用cookie来设置，一个人隔多长时间后再次访问，才算一次阅读量

```python
def blog_detail(request, blog_pk): # 博客细节html界面的渲染；其中blog_pk参数为博客编号(pk意思为外键)
    ...
    if not request.COOKIES.get('blog_%s_readed' % blog_pk):
        blog.readed_num += 1 # 阅读量每次加一
        blog.save() # 博客保存
	...
    response.set_cookie('blog_%s_readed' % blog_pk, 'true') # 设置cookies
    return response
```