# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

class SiteInfo(models.Model):
    site_name = models.CharField(u'网站名称', max_length=30)
    site_slogan = models.CharField('网站广告语', max_length=50)
    site_author = models.CharField(u'网站作者', max_length=30)
    site_keywords = models.CharField(u'网站关键词', max_length=200)
    site_description = models.TextField(u'网站描述')
    site_copyright = models.CharField(u'版权信息', max_length=200, blank=True)
    site_license = models.CharField(u'备案号', max_length=200, blank=True)
    site_email = models.CharField(u'邮箱', max_length=45, blank=True)
    site_phone = models.CharField(u'联系电话', max_length=200, blank=True)

    class Meta:
        db_table = 'django_site_info'
        verbose_name = u'网站信息管理'
        verbose_name_plural = u'网站信息管理'

class MenuInfo(models.Model):
    menu_name = models.CharField(u'菜单名称', max_length=30)
    menu_pid = models.IntegerField(u'上级菜单', null=True)
    menu_link = models.CharField(u'链接', max_length=255, null=True)
    menu_order = models.IntegerField(u'排序', null=True)
    menu_visible = models.IntegerField(u'是否可见', default=1, null=True)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True, null=True)

    class Meta:
        db_table = 'django_menu_info'
        verbose_name = u'菜单管理'
        verbose_name_plural = u'菜单管理'

