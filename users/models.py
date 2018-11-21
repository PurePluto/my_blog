from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name='昵称')
    birthday = models.DateField(null=True, blank=True, verbose_name='生日')
    gender = models.CharField(choices=(('male', '男'), ('female', '女')), max_length=10, verbose_name='性别')
    address = models.CharField(max_length=100, verbose_name='地址')
    mobile = models.CharField(max_length=11, verbose_name='手机号码')
    image = models.ImageField(upload_to='image/%Y/%m', default='image/default.png', verbose_name='头像')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


# 动态绑定
def has_nickname(self):
    if self.nick_name == '':
        return 'error'


def get_nickname_or_username(self):
    if self.nick_name == '':
        return self.username
    else:
        return self.nick_name



UserProfile.has_nickname = has_nickname
UserProfile.get_nickname_or_username = get_nickname_or_username