# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from datetime import datetime, timedelta

from django.db import models
from django.conf import settings

from django.utils import timezone
from django.utils.timesince import timesince

class CrawlerShoppingType(models.Model):
    name = models.CharField(u'分类名称', max_length=200)
    pid = models.IntegerField(u'上级分类', null=True)
    createtime = models.DateTimeField(u'创建时间', auto_now_add=True, null=True)

    def __str__(self):
        return self.name.encode('utf-8')

    class Meta:
        db_table = 'crawler_shopping_type'
        verbose_name = '商品类目'
        verbose_name_plural = '商品类目'

    def formatCreateTime(self):
        return self.createtime.strftime("%Y-%m-%d %H:%M:%S")
    formatCreateTime.short_description = '创建时间'

class CrawlerShoppingInfo(models.Model):
    website = models.CharField('商品来源', max_length=255, blank=True)
    srcid = models.CharField('商品编号', max_length=255, blank=True)
    srclink = models.CharField('商品URL', max_length=255, blank=True)
    shoppingtype = models.ForeignKey(CrawlerShoppingType, verbose_name='商品分类', on_delete=models.CASCADE)
    name = models.CharField('商品名称', max_length=255, blank=True)
    price = models.FloatField('商品价格', blank=True)
    starttime = models.DateTimeField('上架时间', null=True)
    finishtime = models.DateTimeField('下价时间', null=True)
    viewnum = models.IntegerField('浏览', default=0, blank=True)
    createtime = models.DateTimeField('创建时间', auto_now_add=True, null=True)
    updatetime = models.DateTimeField('更新时间', auto_now_add=True, null=True)

    class Meta:
        db_table = 'crawler_shopping_info'
        verbose_name = '商品信息'
        verbose_name_plural = '商品信息'

    def formatCreateTime(self):
        return self.createtime.strftime("%Y-%m-%d %H:%M:%S")
    formatCreateTime.short_description = '创建时间'

