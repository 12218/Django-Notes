# 06--Django笔记--Bootstrap响应式布局

## 一、栅格系统

官网介绍：[栅格系统](https://v3.bootcss.com/css/#grid)

Bootstrap 的栅格系统将网页分成12列，适配各种大小的屏幕

![06-01](.\pictures\06-01.png)

且栅格系统需要被包裹在一个 `.container` 容器中

栅格系统的基本结构是这样的：

```html
<div class="container"> <!-- 栅格系统需要被放在container容器中 -->
    <div class="row"> <!-- 首先定义行，再在行中定义列 -->
        <div class="col-xx-"></div> <!-- 栅格中的列 -->
        <div class="col-xx-"></div> <!-- 栅格中的列 -->
    </div>
</div>
```

将栅格布局更改成如下：

```html
<div class="container"> <!-- 栅格系统需要被放在container容器中 -->
        <div class="row"> <!-- 首先定义行，再在行中定义列 -->
            <div class="col-md-8">  <!-- 博客显示部分 -->
                <p>共有{{ blogs|length }}篇博客</p> <!-- 过滤器 -->
                {% for blog in blogs %} <!-- 这里的blog是从views.py中传入的内容 -->
                    <a href="{% url 'blog_detail' blog.pk %}">
                        <h3>{{ blog.title }}</h3>
                    </a>
                    <p>作者：{{ blog.author }}</p>
                    <p>修改时间：{{ blog.last_updated_time|date:"Y-m-d G:i:s" }}</p>
                    <p>博客类型：{{ blog.blog_type }}</p>
                    <p>{{ blog.content|truncatechars:30 }}</p> <!-- 其中冒号后面的内容表示显示字符长度 -->
                    {% empty %} <!-- 如果为空则执行下面代码 -->
                    <p>--暂无博客，敬请期待--</p>
                {% endfor %}
            </div>
            <div class="col-md-4">  <!-- 博客分类部分 -->
                <h4>博客分类</h4>
                <ul>
                    {% for blog_type in blog_types %}
                        <li>
                            <a href="{% url 'blogs_with_type' blog_type.pk %}">
                                {{ blog_type.type_name }}
                            </a>
                        </li>
                        {% empty %}
                            <li>没有分类</li>
                    {% endfor %}
                </ul>
            </div>
        </div>
    </div>
```

可以将博客布局进行初步处理

![06-02](.\pictures\06-02.png)

## 二、组件

官网介绍：[组件](https://v3.bootcss.com/components/)

做完布局处理之后，想要对各个部分进行划分，可以使用[面板](https://v3.bootcss.com/components/#panels)

```html
<div class="panel panel-default">
  <div class="panel-heading">Panel heading without title</div>
  <div class="panel-body">
    Panel content
  </div>
</div>
```

![06-03](.\pictures\06-03.png)

## 三、屏幕适配问题

当以上的代码制作的页面被放置于小屏幕的时候，右侧的“博客分类”模块会被挤到博客列表下方

如果增加小屏幕的显示方式，则可以避免这种问题 `<div class="col-sm-4 col-md-8">`

而如果希望右边的博客分类模块在超小屏幕的时候隐藏，可以使用官网的[响应式工具](https://v3.bootcss.com/css/#responsive-utilities)

![06-04](.\pictures\06-04.png)

```html
<div class="hidden-xs col-sm-3 col-md-4">  <!-- 博客分类部分 -->
```

## 四、图标

bootstrap图标可参考[官网](https://v3.bootcss.com/components/#glyphicons)

```html
<span class="glyphicon glyphicon-search" aria-hidden="true"></span>
```

更换图标只需要更改class中的内容

## 五、其他

在进行css美化的时候，如果想要让最下面的分割线不显示，可以使用这种方式：

```css
div.blog:not(:last-child) {
    margin-bottom: 2em;
    padding-bottom: 1em;
    border-bottom: 2px solid #ccc;
}
```

