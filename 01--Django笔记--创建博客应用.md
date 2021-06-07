# 01--Django笔记--创建博客应用

## 一、初步创建blog项目

在终端使用命令`django-admin startproject <项目名称>` 进行博客项目的创建。

```python
# 此处建立的blog项目名为mysite
django-admin startproject mysite
```

此时文件夹内产生了一个文件夹，其目录如下：

```bash
(study) root@***:~/Program/Django/study# tree mysite
mysite
├── manage.py
└── mysite
    ├── asgi.py
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py

1 directory, 6 files
```

此时项目创建完毕。

## 二、创建blog应用

使用终端切换到mysite文件夹下，使用命令` python3 manage.py startapp <应用名称>` 进行博客应用的创建。

```python
# 此处建立的应用名为blog
python3 manage.py startapp blog
```

此时文件夹目录结构如下：

```bash
(study) root@***:~/Program/Django/study# tree mysite
mysite
├── blog
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── manage.py
└── mysite
    ├── asgi.py
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py

3 directories, 13 files
```

此时应用创建完毕。

## 三、应用模型的建立

在blog文件夹中 **models.py** 管理的是应用的模型，需要将博客的分类、每篇博客的各个属性(模型)放入其中。

```python
(study) root@***:~/Program/Django/study/mysite/blog# cat models.py 
from django.db import models
from django.contrib.auth.models import User # 导入用户模型

# 设置博客的分类
class BlogType(models.Model):
    type_name = models.CharField(max_length = 15) # 文章博客分类的名称

# 设置每篇博客的属性
class Blog(models.Model):
    title = models.CharField(max_length = 50) # 设置标题，模式为字符，max_length最大长度为50字符
    blog_type = models.ForeignKey(BlogType, on_delete = models.DO_NOTHING) # BlogType是自己设置的博客分类
    content = models.TextField() # 设置文章内容，模式为文本
    author = models.ForeignKey(User, on_delete = models.DO_NOTHING) # 设置作者，作者为外键
    create_time = models.DateTimeField(auto_now_add = True) # 设置创建时间，auto_now_add为“如果新创建一篇文章，将文章时间设为现在时间”
```

## 四、创建超级管理员

在创建超级管理员之前需要先迁移数据库：

```python3 manage.py migrate```

```bash
(study) root@***:~/Program/Django/study/mysite# python3 manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying sessions.0001_initial... OK
```

然后在**项目根目录**下依次使用以下几条命令，创建超级管理员：

```
python3 manage.py createsuperuser
```
输入命令之后按提示输入需要的信息即可：

```bash
(study) root@***:~/Program/Django/study/mysite# python3 manage.py createsuperuser
Username (leave blank to use 'root'): 12218
Email address: lbr12218@outlook.com
Password: 
Password (again): 
This password is too short. It must contain at least 8 characters.
This password is entirely numeric.
Bypass password validation and create user anyway? [y/N]: y
Superuser created successfully.
```

## 五、将应用添加到setting

打开./mysite/mysite/settings.py，将应用添加到数组 INSTALLED_APPS 数组中，应用才能够被使用。

![01-01](https://img-blog.csdnimg.cn/20210607213250562.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NDMzODc4MA==,size_16,color_FFFFFF,t_70#pic_center)


插入之后，需要使用命令生成迁移文件：

```bash
(study) root@***:~/Program/Django/study/mysite# python3 manage.py makemigrations
Migrations for 'blog':
  blog/migrations/0001_initial.py
    - Create model BlogType
    - Create model Blog
```

此时产生了迁移文件`blog/migrations/0001_initial.py`。



然后使用`python3 manage.py migrate`使迁移生效：

```bash
(study) root@***:~/Program/Django/study/mysite# python3 manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, blog, contenttypes, sessions
Running migrations:
  Applying blog.0001_initial... OK
```

## 六、运行

使用命令`python3 manage.py runserver [端口号]`运行，此时可以在浏览器输入`127.0.0.1:端口号`查看运行结果。

![01-02](https://img-blog.csdnimg.cn/20210607213310140.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NDMzODc4MA==,size_16,color_FFFFFF,t_70#pic_center)


进入`127.0.0.1:端口号/admin`可以进入超级管理员的登录界面。

在此可以增加删除博文。

![01-03](https://img-blog.csdnimg.cn/20210607213323542.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NDMzODc4MA==,size_16,color_FFFFFF,t_70#pic_center)


## 七、其他

在./mysite/mysite/settings.py中可以设置界面中文及时区：

![01-04](https://img-blog.csdnimg.cn/2021060721334642.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NDMzODc4MA==,size_16,color_FFFFFF,t_70#pic_center)


设置博客分类可以显示：

![01-05](https://img-blog.csdnimg.cn/20210607213506947.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NDMzODc4MA==,size_16,color_FFFFFF,t_70#pic_center)

