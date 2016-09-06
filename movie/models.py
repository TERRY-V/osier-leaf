# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from datetime import datetime

from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.

class CrawlerMovieInfo(models.Model):
    id = models.IntegerField('电影编号')
    website = models.CharField('网站来源', max_length=255, blank=True)
    srcid = models.CharField('采集编号', primary_key=True, max_length=255, blank=True)
    srclink = models.CharField('采集URL', max_length=255, blank=True)
    type = models.IntegerField('一级分类', blank=True, null=True)
    extratype = models.IntegerField('二级分类', blank=True, null=True)
    moviename = models.CharField('电影名称', max_length=255, blank=True)
    starring = models.TextField('电影主演', blank=True)
    language = models.CharField('电影语言', max_length=255, blank=True)
    area = models.CharField('地区', max_length=255, blank=True)
    director = models.CharField('导演', max_length=255, blank=True)
    movietype = models.CharField('类型', max_length=255, blank=True)
    writer = models.CharField('编剧', max_length=255, blank=True)
    release_company = models.TextField('发行公司', blank=True)
    release_time = models.DateField('上映时间', blank=True, null=True)
    manufacture_company = models.TextField('制片公司', blank=True)
    alias = models.TextField('别名', blank=True)
    score = models.FloatField('得分')
    story = models.TextField('剧情简介', blank=True)
    viewnum = models.IntegerField('浏览', blank=True)
    supportnum = models.IntegerField('支持', blank=True)
    againstnum = models.IntegerField('反对', blank=True)
    createtime = models.DateTimeField('创建时间', blank=True, null=True)
    updatetime = models.DateTimeField('更新时间', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'crawler_movie_info'
        verbose_name = '电影信息'
        verbose_name_plural = '电影信息'

    def labels_as_list(self):
        return self.movietype.split('/')

    def get_time_string(self):
        return self.createtime.strftime("%Y-%m-%d %H:%M:%S")

    def get_release_time_string(self):
        if self.release_time:
            return self.release_time.strftime("%Y-%m-%d")
        else:
            return ""

class CrawlerMoviePlaylink(models.Model):
    id = models.IntegerField(primary_key=True)
    srcid = models.ForeignKey('CrawlerMovieInfo', db_column='srcid', on_delete=models.CASCADE)
    linkname = models.CharField('电影来源', max_length=255)
    playlink = models.CharField('播放链接', max_length=255)
    createtime = models.DateTimeField('创建时间', blank=True, null=True)
    updatetime = models.DateTimeField('更新时间', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'crawler_movie_playlink'
        verbose_name = '播放链接'
        verbose_name_plural = '播放链接'

class CrawlerMovieImg(models.Model):
    id = models.IntegerField(primary_key=True)
    srcid = models.ForeignKey('CrawlerMovieInfo', db_column='srcid', on_delete=models.CASCADE)
    imgid = models.CharField('图片ID', max_length=255)
    imglink = models.CharField('图片链接', max_length=255)
    imgpath = models.CharField('图片路径', max_length=255)
    createtime = models.DateTimeField('创建时间', blank=True, null=True)
    updatetime = models.DateTimeField('更新时间', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'crawler_movie_img'
        verbose_name = '电影图片'
        verbose_name_plural = '电影图片'

class CrawlerMovieComment(models.Model):
    id = models.IntegerField(primary_key=True)
    srcid = models.ForeignKey('CrawlerMovieInfo', db_column='srcid', on_delete=models.CASCADE)
    comment = models.TextField('评论内容', blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='用户')
    supportnum = models.IntegerField('支持', blank=True)
    createtime = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'crawler_movie_comment'
        verbose_name = '电影评论'
        verbose_name_plural = '电影评论'

