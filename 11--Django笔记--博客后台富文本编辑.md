# 11--Django笔记--博客后台富文本编辑

## 一、允许html加载

如果需要让博客文章中的html加载出来，可以使用过滤器，将传入的文章内容标为安全

```html
<!-- blog_detail.html -->
<div class="blog-content">
    {{ blog.content|safe }}
</div>
```

但是此时，博客列表中的前70个字符的文章内容中，也会显示html的标签，故此需要使用过滤器处理掉

```html
<!-- blog_list.html -->
<p>{{ blog.content|striptags|truncatechars:70 }}</p> <!-- 其中冒号后面的内容表示显示字符长度 -->
```

![11-01](https://img-blog.csdnimg.cn/20210703222025107.png#pic_center)


![11-02](https://img-blog.csdnimg.cn/202107032220381.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NDMzODc4MA==,size_16,color_FFFFFF,t_70#pic_center)


但是以上这种方法还是会带来编辑困难，因为写博客的时候需要使用html来写

## 二、使用django-ckeditor

### 1. 安装django-ckeditor

```bash
(study) root@***:~/Program/Django/study/mysite# pip3 install --index https://mirrors.aliyun.com/pypi/simple django-ckeditor
```

### 2. 注册应用

在使用之前，还需要进行注册应用

![11-03](https://img-blog.csdnimg.cn/20210703222052639.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NDMzODc4MA==,size_16,color_FFFFFF,t_70#pic_center)


### 3. 配置model

把博客内容字段改成 `RichTextField` 

![11-04](https://img-blog.csdnimg.cn/20210703222109778.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NDMzODc4MA==,size_16,color_FFFFFF,t_70#pic_center)


接着迁移数据库

```bash
(study) root@***:~/Program/Django/study/mysite# python3 manage.py makemigrations
Migrations for 'blog':
  blog/migrations/0003_auto_20210703_2136.py
    - Alter field blog_type on blog
    - Alter field content on blog
(study) root@***:~/Program/Django/study/mysite# python3 manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, blog, contenttypes, sessions
Running migrations:
  Applying blog.0003_auto_20210703_2136... OK
(study) root@***:~/Program/Django/study/mysite#
```

此时再次打开博客编辑页面，就可以看到内容字段可以进行富文本编辑

![11-05](https://img-blog.csdnimg.cn/20210703222125589.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NDMzODc4MA==,size_16,color_FFFFFF,t_70#pic_center)


## 4. 添加图片上传功能

但是现在编辑博客页面中的添加图片，只能使用url添加

所以需要添加上传图片的功能

### 1. 安装pillow

如果不安装这个库，上传图片的过程中可能会出现错误

```bash
(study) root@***:~/Program/Django/study/mysite# pip3 install --index https://mirrors.aliyun.com/pypi/simple pillow
Looking in indexes: https://mirrors.aliyun.com/pypi/simple
Collecting pillow
  Downloading https://mirrors.aliyun.com/pypi/packages/d5/21/c700a8ecdf34661defd640d068a9d3a2b2290b07625ab0d82b1c8faa6f92/Pillow-8.3.0-cp38-cp38-manylinux_2_5_x86_64.manylinux1_x86_64.whl (3.0 MB)
     |████████████████████████████████| 3.0 MB 3.8 MB/s 
Installing collected packages: pillow
Successfully installed pillow-8.3.0
```

### 2. 注册应用

![11-06](https://img-blog.csdnimg.cn/20210703222145221.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NDMzODc4MA==,size_16,color_FFFFFF,t_70#pic_center)


### 3. 配置上传路径

打开 **settings.py** ，添加路径

![11-07](https://img-blog.csdnimg.cn/20210703222159633.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NDMzODc4MA==,size_16,color_FFFFFF,t_70#pic_center)


### 4. 配置url

上传图片文件时，也需要有一个上传url

![11-08](https://img-blog.csdnimg.cn/20210703222211486.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NDMzODc4MA==,size_16,color_FFFFFF,t_70#pic_center)


### 5. 配置model

 `RichTextField` 中不允许上传图片，所以需要换成 `RichTextUploadingField`

![11-09](https://img-blog.csdnimg.cn/20210703222227387.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NDMzODc4MA==,size_16,color_FFFFFF,t_70#pic_center)


之后迁移数据库使之生效

就可以看到上传模块

![11-10](https://img-blog.csdnimg.cn/20210703222243300.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NDMzODc4MA==,size_16,color_FFFFFF,t_70#pic_center)


![11-11](https://img-blog.csdnimg.cn/20210703222301975.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NDMzODc4MA==,size_16,color_FFFFFF,t_70#pic_center)
