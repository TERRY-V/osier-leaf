# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from datetime import datetime

from django.db import models
from django.conf import settings
from django.utils import timezone

class CrawlerHealthInfo(models.Model):
    id = models.IntegerField('信息编号')
    website = models.CharField('网站来源', max_length=255, blank=True)
    srcid = models.CharField('采集编号', primary_key=True, max_length=255, blank=True)
    srclink = models.CharField('采集URL', max_length=255, blank=True)
    type = models.IntegerField('一级分类', blank=True, null=True)
    extratype = models.IntegerField('二级分类', blank=True, null=True)
    title = models.CharField('标题', max_length=255, blank=True)
    summary = models.TextField('摘要', max_length=2000, blank=True)
    viewnum = models.IntegerField('浏览', blank=True)
    supportnum = models.IntegerField('支持', blank=True)
    againstnum = models.IntegerField('反对', blank=True)
    createtime = models.DateTimeField('创建时间', blank=True, null=True)
    updatetime = models.DateTimeField('更新时间', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'crawler_health_info'
        verbose_name = '健康信息'
        verbose_name_plural = '健康信息'

    def get_time_string(self):
        return self.createtime.strftime("%Y-%m-%d %H:%M:%S")

class CrawlerHealthArticle(models.Model):
    id = models.IntegerField(primary_key=True)
    srcid = models.ForeignKey('CrawlerHealthInfo', db_column='srcid', on_delete=models.CASCADE)
    question = models.CharField('关注问题', max_length=255)
    answer = models.TextField('关注答案')
    createtime = models.DateTimeField('创建时间', blank=True, null=True)
    updatetime = models.DateTimeField('更新时间', blank=True, null=True)

    def paragraph_as_list(self):
        text = self.answer.replace('。', '。\n')
        text = text.replace('？', '？\n')
        text = text.replace('！', '!\n')
        return text.split('\n')

    class Meta:
        managed = False
        db_table = 'crawler_health_article'
        verbose_name = '关注问题'
        verbose_name_plural = '关注问题'

class CrawlerHealthComment(models.Model):
    id = models.IntegerField(primary_key=True)
    srcid = models.ForeignKey('CrawlerHealthInfo', db_column='srcid', on_delete=models.CASCADE)
    comment = models.TextField('评论内容', blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='用户')
    supportnum = models.IntegerField('支持', blank=True)
    createtime = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'crawler_health_comment'
        verbose_name = '健康评论'
        verbose_name_plural = '健康评论'

