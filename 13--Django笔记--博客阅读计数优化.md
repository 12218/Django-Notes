# 13--Django笔记--博客阅读计数优化

上一篇笔记中，博客阅读计数不能达到统计同一天阅读数量的功能，且编辑时间会随阅读数量刷新，故此进行优化

## 一、固定模型计数方式

### 1. 创建模型

把阅读量单独作为一个模型，可以让阅读量和博客的创建时间之间不再有联系

在 **models.py** 文件中加入新模型

```python
# 设置阅读量模型
class ReadNum(models.Model):
    read_num = models.IntegerField(default = 0)
    blog = models.OneToOneField(Blog, on_delete = models.DO_NOTHING) # 一对一模式，每篇博客对应一个阅读量
```

迁移数据库使之生效

之后在 **admin.py** 为新建的模型注册

```python
# admin.py
...
from .models import BlogType, Blog, ReadNum # 引入创建好的博客模型和博客分类、阅读量
...
@admin.register(ReadNum)
class BlogAdmin(admin.ModelAdmin): # 注册阅读量模型
    list_display = ('read_num', 'blog')
```

### 2. 管理员界面显示阅读数量

修改模型和注册，让字段可以在管理员界面显示

修改模型 **models.py** ：

```python
# 设置每篇博客的属性
class Blog(models.Model):
    ...
    def read_num(self):
        return self.readnum.read_num # 显示阅读数量

    def __str__(self) -> str:
        return "<Blog: %s>" % self.title
    ...
```

然后修改注册 **admin.py** ：

![13-01](https://img-blog.csdnimg.cn/20210708194513789.png#pic_center)


### 3. 创建/增加阅读数量

修改 **views.py** 文件中的blog_detail函数，让不存在阅读记录的博客创建阅读记录，存在记录的博客，阅读量加1

```python
def blog_detail(request, blog_pk): # 博客细节html界面的渲染；其中blog_pk参数为博客编号(pk意思为外键)
    blog = get_object_or_404(Blog, id = blog_pk) # get_object_or_404()在无法取到object的时候返回404界面
    if not request.COOKIES.get('blog_%s_readed' % blog_pk):
        # blog.readed_num += 1 # 阅读量每次加一
        # blog.save() # 博客保存
        if ReadNum.objects.filter(blog = blog).count(): # 如果存在阅读记录，加1
            readnum = ReadNum.objects.get(blog = blog)
        else: # 如果不存在阅读记录
            readnum = ReadNum() # 创建阅读记录
            readnum.blog = blog
        readnum.read_num += 1 # 阅读数量加1
        readnum.save()
        ...
```

修改完之后，还要修改前端页面使其显示：

修改 **blog_detail.html** 文件，此处即可直接调用模型中新创建的的方法

```html
<li>阅读量：{{ blog.read_num }}</li>
```

修改结果：

![13-02](https://img-blog.csdnimg.cn/20210708194531244.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NDMzODc4MA==,size_16,color_FFFFFF,t_70#pic_center)


可以发现问题，不存在的记录会不显示，而是报一个错误“没有read_num”，可以捕获这个错误，然后返回0：

```python
...
from django.core.exceptions import ObjectDoesNotExist
...
# 设置每篇博客的属性
class Blog(models.Model):
    ...
    def get_read_num(self):
        # return self.readnum.read_num # 显示阅读数量
        try:
            return self.readnum.read_num # 显示阅读数量
        except ObjectDoesNotExist:
            return 0
```

即可正常显示

## 二、ContentType

### 1. 创建应用

首先创建应用 **read_statistics** 

```bash
python3 manage.py startapp read_statistics
```

修改模型 **models.py** ，使其关联外键：

```python
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.
class ReadNum(models.Model):
    read_num = models.IntegerField(default = 0)

    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
```

**settings.py** 添加应用：

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',
    'ckeditor',
    'ckeditor_uploader',
    'read_statistics',
]
```

之后迁移数据库使之生效

再在 **admin.py** 注册应用，使管理员界面可以显示此页面：

```python
from django.contrib import admin
from .models import ReadNum

# Register your models here.
@admin.register(ReadNum)
class ReadNumAdmin(admin.ModelAdmin): # 注册阅读量模型
    list_display = ('read_num', 'content_object')
```

现在打开django后台，即可见到应用

![13-03](https://img-blog.csdnimg.cn/20210708194558409.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NDMzODc4MA==,size_16,color_FFFFFF,t_70#pic_center)


### 2. 关联应用

修改 **models.py** ：

```python
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User # 导入用户模型
# from ckeditor.fields import RichTextField # 富文本编辑字段
from ckeditor_uploader.fields import RichTextUploadingField # 可上传文件的富文本编辑字段
from django.contrib.contenttypes.models import ContentType
from read_statistics.models import ReadNum

# 设置博客的分类
class BlogType(models.Model):
    type_name = models.CharField(max_length = 15) # 文章博客分类的名称

    def __str__(self) -> str:
        return self.type_name # 设置博客类型在超级管理员界面可以显示

# 设置每篇博客的属性
class Blog(models.Model):
    title = models.CharField(max_length = 50) # 设置标题，模式为字符，max_length最大长度为50字符
    blog_type = models.ForeignKey(BlogType, on_delete = models.DO_NOTHING, related_name = 'blog_blog') # BlogType是自己设置的博客分类
    content = RichTextUploadingField() # 设置文章内容，模式为富文本
    author = models.ForeignKey(User, on_delete = models.DO_NOTHING) # 设置作者，作者为外键
    # readed_num = models.IntegerField(default = 0) # 博客阅读次数
    create_time = models.DateTimeField(auto_now_add = True) # 设置创建时间，auto_now_add为“如果新创建一篇文章，将文章时间设为现在时间”
    last_updated_time = models.DateTimeField(auto_now_add = True)
    def get_read_num(self):
        ct = ContentType.objects.get_for_model(Blog)
        readnum = ReadNum.onjects.get(content_type = ct, object_id = self.pk)
        return readnum.read_num

    def __str__(self) -> str:
        return "<Blog: %s>" % self.title

    class Meta:
        ordering = ['-create_time']
```

同时修改 **admin.py** 使其在管理界面显示：

```python
from django.contrib import admin
# from .models import BlogType, Blog, ReadNum # 引入创建好的博客模型和博客分类、阅读量
from .models import BlogType, Blog # 引入创建好的博客模型和博客分类、阅读量

# 在此进行博客模型的注册
# Register your models here.
@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin): # 注册博客分类
    list_display = ('id', 'type_name') # 此处放入的值为在超级管理员界面显示的信息

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin): # 注册博客模型
    # list_display = ('title', 'blog_type', 'author', 'get_read_num', 'create_time', 'last_updated_time') # 此处放入的值为在超级管理员界面显示的信息
    list_display = ('id', 'title', 'blog_type', 'author', 'get_read_num', 'create_time', 'last_updated_time') # 此处放入的值为在超级管理员界面显示的信息
```

此时，打开管理界面，已经可以看到修改结果：

![13-04](https://img-blog.csdnimg.cn/20210708194615274.png#pic_center)


但是，没有设置过阅读数量的博客还是不能显示，需要使用捕获错误的方式处理掉

```python
def get_read_num(self):
        try:
            ct = ContentType.objects.get_for_model(Blog)
            readnum = ReadNum.objects.get(content_type = ct, object_id = self.pk)
            return readnum.read_num
        except ObjectDoesNotExist:
            return 0
```

关联阅读数量：

```python
def blog_detail(request, blog_pk): # 博客细节html界面的渲染；其中blog_pk参数为博客编号(pk意思为外键)
    blog = get_object_or_404(Blog, id = blog_pk) # get_object_or_404()在无法取到object的时候返回404界面
    if not request.COOKIES.get('blog_%s_readed' % blog_pk):
        ct = ContentType.objects.get_for_model(Blog)
        if ReadNum.objects.filter(content_type = ct, object_id = blog.pk).count(): # 如果存在阅读记录，加1
            readnum = ReadNum.objects.get(content_type = ct, object_id = blog.pk)
        else: # 如果不存在阅读记录
            readnum = ReadNum(content_type = ct, object_id = blog.pk) # 创建阅读记录
        readnum.read_num += 1 # 阅读数量加1
        readnum.save()
```
