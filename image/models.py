# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from datetime import datetime

from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.

class CrawlerImageInfo(models.Model):
    id = models.IntegerField('图片编号')
    website = models.CharField('网站来源', max_length=255, blank=True)
    srcid = models.CharField('采集编号', primary_key=True, max_length=255, blank=True)
    srclink = models.CharField('采集URL', max_length=255, blank=True)
    type = models.IntegerField('一级分类', blank=True, null=True)
    extratype = models.IntegerField('二级分类', blank=True, null=True)
    title = models.CharField('图片标题', max_length=255, blank=True)
    imgid = models.CharField('图片ID', max_length=255, blank=True)
    imgpath = models.CharField('图片路径', max_length=255, blank=True)
    imglink = models.CharField('图片链接', max_length=255, blank=True)
    imgsize = models.CharField('图片尺寸', max_length=255, blank=True)
    createtime = models.DateTimeField('创建时间', blank=True, null=True)
    updatetime = models.DateTimeField('更新时间', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'crawler_image_info'
        verbose_name = '图片信息'
        verbose_name_plural = '图片信息'

    def get_time_string(self):
        return self.createtime.strftime("%Y-%m-%d %H:%M:%S")

class CrawlerImageCategory(models.Model):
    id = models.IntegerField('图片编号', primary_key=True)
    type = models.IntegerField('分类编号')
    summary = models.CharField('分类名称', max_length=255, blank=True)
    pid = models.IntegerField('上级分类')
    createtime = models.DateTimeField('创建时间', blank=True, null=True)
    updatetime = models.DateTimeField('更新时间', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'crawler_image_category'
        verbose_name = '分类信息'
        verbose_name_plural = '分类信息'

