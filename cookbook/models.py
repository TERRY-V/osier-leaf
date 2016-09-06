# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from datetime import datetime, timedelta

from django.db import models
from django.conf import settings

from django.utils import timezone
from django.utils.timesince import timesince

class CrawlerCookbookInfo(models.Model):
    id = models.IntegerField('美食编号')
    website = models.CharField('网站来源', max_length=255, blank=True)
    srcid = models.CharField('采集编号', primary_key=True, max_length=255, blank=True)
    srclink = models.CharField('采集URL', max_length=255, blank=True)
    type = models.IntegerField('一级分类', blank=True, null=True)
    extratype = models.IntegerField('二级分类', blank=True, null=True)
    name = models.CharField('美食名称', max_length=255, blank=True)
    comment = models.TextField('美食评论', blank=True)
    main_spice = models.TextField('美食主料', blank=True)
    assist_spice = models.TextField('美食辅料', blank=True)
    cooks = models.CharField('厨具', max_length=255, blank=True)
    classify = models.CharField('分类', max_length=255, blank=True)
    trick = models.TextField('小技巧', blank=True)
    viewnum = models.IntegerField('浏览', blank=True)
    supportnum = models.IntegerField('支持', blank=True)
    againstnum = models.IntegerField('反对', blank=True)
    createtime = models.DateTimeField('创建时间', blank=True, null=True)
    updatetime = models.DateTimeField('更新时间', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'crawler_cookbook_info'
        verbose_name = '美食信息'
        verbose_name_plural = '美食信息'

    def labels_as_list(self):
        return self.classify.split('\n')

    def get_time_string(self):
        timedelta = timesince(self.createtime).split(',')[0]
        if timedelta.find('minute') != -1:
            minutes = timedelta.split('\xa0')[0]
            if minutes <> '0':
                return minutes + '分钟前'
            else:
                return '刚刚'
        elif timedelta.find('hour') != -1:
            return timedelta.split('\xa0')[0] + '小时前'
        elif timedelta.find('day') != -1:
            return timedelta.split('\xa0')[0] + '天前'
        elif timedelta.find('month') != -1:
            return timedelta.split('\xa0')[0] + '个月前'
        elif timedelta.find('week') != -1:
            return timedelta.split('\xa0')[0] + '周前'
        elif timedelta.find('year') != -1:
            return timedelta.split('\xa0')[0] + '年前'
        else:
            return timedelta

class CrawlerCookbookStep(models.Model):
    id = models.IntegerField(primary_key=True)
    srcid = models.ForeignKey('CrawlerCookbookInfo', db_column='srcid', on_delete=models.CASCADE)
    imgid = models.CharField('图片ID', max_length=255)
    imglink = models.CharField('图片链接', max_length=255)
    imgpath = models.CharField('图片路径', max_length=255)
    step_method = models.TextField('步骤', blank=True)
    createtime = models.DateTimeField('创建时间', blank=True, null=True)
    updatetime = models.DateTimeField('更新时间', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'crawler_cookbook_step'
        verbose_name = '做菜方法'
        verbose_name_plural = '做菜方法'

class CrawlerCookbookImg(models.Model):
    id = models.IntegerField(primary_key=True)
    srcid = models.ForeignKey('CrawlerCookbookInfo', db_column='srcid', on_delete=models.CASCADE)
    imgid = models.CharField('图片ID', max_length=255)
    imglink = models.CharField('图片链接', max_length=255)
    imgpath = models.CharField('图片路径', max_length=255)
    imgtitle = models.TextField('标题', blank=True)
    createtime = models.DateTimeField('创建时间', blank=True, null=True)
    updatetime = models.DateTimeField('更新时间', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'crawler_cookbook_img'
        verbose_name = '美食图片'
        verbose_name_plural = '美食图片'

class CrawlerCookbookComment(models.Model):
    id = models.IntegerField(primary_key=True)
    srcid = models.ForeignKey('CrawlerCookbookInfo', db_column='srcid', on_delete=models.CASCADE)
    comment = models.TextField('评论内容', blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='用户')
    supportnum = models.IntegerField('支持', blank=True)
    createtime = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'crawler_cookbook_comment'
        verbose_name = '美食评论'
        verbose_name_plural = '美食评论'

