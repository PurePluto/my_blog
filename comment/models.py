from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from users.models import UserProfile
# Create your models here.


class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveSmallIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.TextField(verbose_name='评论内容')
    comment_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(UserProfile, related_name='comments' , on_delete=models.CASCADE, verbose_name='用户')

    root = models.ForeignKey('self', related_name='root_comment', null=True, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, on_delete=models.CASCADE)
    reply_to = models.ForeignKey(UserProfile, related_name='replies', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = '评论内容'
        verbose_name_plural = verbose_name
        ordering = ['comment_time']