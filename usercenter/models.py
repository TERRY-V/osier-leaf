# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class string_with_title(str):
    def __new__(cls, value, title):
        instance = str.__new__(cls, value)
        instance._title = title
        return instance

    def title(self):
        return self._title

    __copy__ = lambda self: self
    __deepcopy__ = lambda self, memodict: self

class User(AbstractUser):
    img = models.CharField(max_length=200, default='/static/avatar/default.gif', verbose_name='头像地址')
    intro = models.CharField(max_length=200, blank=True, null=True, verbose_name='简介')

    class Meta(AbstractUser.Meta):
        app_label = string_with_title('usercenter', "用户管理")
