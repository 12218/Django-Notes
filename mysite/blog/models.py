from django.db import models
from django.contrib.auth.models import User # 导入用户模型
# from ckeditor.fields import RichTextField # 富文本编辑字段
from ckeditor_uploader.fields import RichTextUploadingField # 可上传文件的富文本编辑字段

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
    create_time = models.DateTimeField(auto_now_add = True) # 设置创建时间，auto_now_add为“如果新创建一篇文章，将文章时间设为现在时间”
    last_updated_time = models.DateTimeField(auto_now_add = True)

    def __str__(self) -> str:
        return "<Blog: %s>" % self.title

    class Meta:
        ordering = ['-create_time']