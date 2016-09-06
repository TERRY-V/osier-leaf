# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

class Website(models.Model):
    site_name = models.CharField('网站名称', max_length=30)
    site_slogan = models.CharField('网站广告语', max_length=50)
    site_author = models.CharField('网站作者', max_length=30)
    site_keywords = models.CharField('网站关键词', max_length=200)
    site_description = models.TextField('网站描述')
    site_copyright = models.CharField('版权信息', max_length=200, blank=True)
    site_license = models.CharField('备案号', max_length=200, blank=True)
    site_declaration = models.TextField('负责声明', blank=True)
    site_address = models.CharField('联系地址', max_length=200, blank=True)
    site_zip = models.CharField('邮编', max_length=45, blank=True)
    site_email = models.CharField('邮箱', max_length=45, blank=True)
    site_phone = models.CharField('联系电话', max_length=200, blank=True)

    class Meta:
        managed = False
        verbose_name = '网站信息管理'
        verbose_name_plural = '网站信息管理'

class FriendLinks(models.Model):
    site = models.ForeignKey(Website, on_delete=models.CASCADE)
    linkname = models.CharField('链接名称', max_length=200, blank=True)
    linkurl = models.CharField('链接地址', max_length=200, blank=True)
    createtime = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '友情链接管理'
        verbose_name_plural = '友情链接管理'

class Column(models.Model):
    column_name = models.CharField('栏目名称', max_length=30)
    column_url = models.CharField('栏目Url', max_length=200)
    column_icon = models.CharField('栏目Icon', max_length=100)
    column_order = models.IntegerField('栏目排序')
    column_status = models.IntegerField('栏目状态')
    column_search = models.IntegerField('搜索状态', default=0)

    class Meta:
        verbose_name = '栏目管理'
        verbose_name_plural = '栏目管理'

class News(models.Model):
    news_time = models.CharField('新闻时间', max_length=50, blank=True)
    news_title = models.CharField('新闻标题', max_length=200, blank=True)
    createtime = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '新闻动态管理'
        verbose_name_plural = '新闻动态管理'

