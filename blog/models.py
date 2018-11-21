from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

from users.models import UserProfile
from read_statistics.models import ReadNum
from read_statistics.models import ReadNumExpandMethod, ReadDetail
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='分类')

    class Meta:
        verbose_name = '博客分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Blog(models.Model, ReadNumExpandMethod):
    title = models.CharField(max_length=50, verbose_name='标题')
    author = models.ForeignKey(UserProfile, verbose_name='作者', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.CASCADE)
    read_details = GenericRelation(ReadDetail)
    content = RichTextUploadingField(verbose_name='正文')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now_add=True, verbose_name='最后一次更新时间')

    # def get_read_num(self):
    #     ct = ContentType.objects.get_for_model(Blog)
    #     readnum = ReadNum.objects.get(content_type=ct, object_id=self.pk)
    #     return readnum.read_num
    def get_url(self):
        return reverse('blog_detail', kwargs={'blog.pk': self.pk})

    def get_email(self):
        return self.author.email

    class Meta:
        verbose_name = '博客管理'
        verbose_name_plural = verbose_name
        ordering = ['-create_time']

    def __str__(self):
        return "<Blog:1>".format(self.title)
