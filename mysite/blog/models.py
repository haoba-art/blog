from django.db import models
from django.utils import timezone
from datetime import datetime

# Create your models here.
# 管理员model
class Admin(models.Model):
    """ 管理员 """
    username = models.CharField(verbose_name="用户名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)

    def __str__(self):
        return self.username


# 用户model
class UserInfo(models.Model):
    name = models.CharField(verbose_name="姓名", max_length=16)
    password = models.CharField(verbose_name="密码", max_length=64)
    age = models.IntegerField(verbose_name="年龄")
    gender_choices = (
        (1, "男"),
        (2, "女"),
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)
    create_time = models.DateField(verbose_name="注册时间", default=datetime.now)


# 文章model
class Article(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    body = models.TextField()
    created = models.DateTimeField(default=datetime.now)
    updated = models.DateTimeField(auto_now=True)




