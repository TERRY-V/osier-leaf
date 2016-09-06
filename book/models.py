# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from datetime import datetime

from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.

class CrawlerBookInfo(models.Model):
    id = models.IntegerField('图书编号')
    website = models.CharField('网站来源', max_length=255, blank=True)
    srcid = models.CharField('采集编号', primary_key=True, max_length=255, blank=True)
    srclink = models.CharField('采集URL', max_length=255, blank=True)
    type = models.IntegerField('一级分类', blank=True, null=True)
    extratype = models.IntegerField('二级分类', blank=True, null=True)
    bookname = models.CharField('图书名称', max_length=255, blank=True)
    subtitle = models.CharField('副标题', max_length=255, blank=True)
    originname = models.CharField('原作名', max_length=255, blank=True)
    author = models.CharField('作者', max_length=255, blank=True)
    translator = models.CharField('译者', max_length=255, blank=True)
    press = models.CharField('出版社', max_length=255, blank=True)
    year = models.DateField('出版年', max_length=255, blank=True)
    page = models.CharField('页数', max_length=255, blank=True)
    price = models.CharField('定价', max_length=255, blank=True)
    collection = models.CharField('丛书', max_length=255, blank=True)
    bidding = models.CharField('装帧', max_length=255, blank=True)
    isbn = models.CharField('ISBN', max_length=255, blank=True)
    score = models.FloatField('得分')
    content_intro = models.TextField('内容简介', blank=True)
    author_intro = models.TextField('作者简介', blank=True)
    dir = models.TextField('目录', blank=True)
    reviewlink = models.CharField('评论链接', max_length=255, blank=True)
    viewnum = models.IntegerField('浏览', blank=True)
    supportnum = models.IntegerField('支持', blank=True)
    againstnum = models.IntegerField('反对', blank=True)
    createtime = models.DateTimeField('创建时间', blank=True, null=True)
    updatetime = models.DateTimeField('更新时间', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'crawler_book_info'
        verbose_name = '图书信息'
        verbose_name_plural = '图书信息'

    def get_time_string(self):
        return self.createtime.strftime("%Y-%m-%d %H:%M:%S")

    def get_year_string(self):
        return self.year.strftime("%Y-%m-%d")

class CrawlerBookBuy(models.Model):
    id = models.IntegerField(primary_key=True)
    srcid = models.ForeignKey('CrawlerBookInfo', db_column='srcid', on_delete=models.CASCADE)
    link = models.CharField('链接', max_length=255)
    sitename = models.CharField('站点', max_length=255)
    dyprice = models.CharField('价格', max_length=255)
    createtime = models.DateTimeField('创建时间', blank=True, null=True)
    updatetime = models.DateTimeField('更新时间', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'crawler_book_buy'
        verbose_name = '购买链接'
        verbose_name_plural = '购买链接'

class CrawlerBookImg(models.Model):
    id = models.IntegerField(primary_key=True)
    srcid = models.ForeignKey('CrawlerBookInfo', db_column='srcid', on_delete=models.CASCADE)
    imgid = models.CharField('图片ID', max_length=255)
    imglink = models.CharField('图片链接', max_length=255)
    imgpath = models.CharField('图片路径', max_length=255)
    createtime = models.DateTimeField('创建时间', blank=True, null=True)
    updatetime = models.DateTimeField('更新时间', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'crawler_book_img'
        verbose_name = '电影图片'
        verbose_name_plural = '电影图片'

class CrawlerBookComment(models.Model):
    id = models.IntegerField(primary_key=True)
    srcid = models.ForeignKey('CrawlerBookInfo', db_column='srcid', on_delete=models.CASCADE)
    comment = models.TextField('评论内容', blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='用户')
    supportnum = models.IntegerField('支持', blank=True)
    createtime = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'crawler_book_comment'
        verbose_name = '电影评论'
        verbose_name_plural = '电影评论'

