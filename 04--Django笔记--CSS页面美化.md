# 04--Django笔记--CSS页面美化

## 一、CSS静态文件

### 方式一：

在Django项目中，如果需要在html中调用静态文件(文件图片、css样式文件、JavaScript文件等)，需要提前设置

打开 /mysite/mysite/settings.py 文件进行修改：

![04-01](https://img-blog.csdnimg.cn/2021061222362037.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NDMzODc4MA==,size_16,color_FFFFFF,t_70#pic_center)

在 **settings.py** 文件中设置过静态文件路径，则可以在html中直接调用：

![04-02](https://img-blog.csdnimg.cn/20210612223657146.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NDMzODc4MA==,size_16,color_FFFFFF,t_70#pic_center)


### 方式二：

直接修改html文件，在html文件首部添加代码 `{% load static %}` 

并且将静态文件调用链接修改成这个样子 `href="{% static 'css/base.css' %}` 

![04-03](https://img-blog.csdnimg.cn/20210612223723626.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NDMzODc4MA==,size_16,color_FFFFFF,t_70#pic_center)

也可以对静态文件进行调用
