# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from datetime import datetime

from django.db import models
from django.conf import settings
from django.utils import timezone

class CrawlerStarInfo(models.Model):
    id = models.IntegerField('明星编号')
    website = models.CharField('网站来源', max_length=255, blank=True)
    srcid = models.CharField('采集编号', primary_key=True, max_length=255, blank=True)
    srclink = models.CharField('采集URL', max_length=255, blank=True)
    type = models.IntegerField('一级分类', blank=True, null=True)
    extratype = models.IntegerField('二级分类', blank=True, null=True)
    name = models.CharField('明星名', max_length=255, blank=True)
    engname = models.CharField('英文名', max_length=255, blank=True)
    aliase = models.CharField('别名', max_length=255, blank=True)
    gender = models.CharField('性别', max_length=255, blank=True)
    birthday = models.CharField('生日', max_length=255, blank=True)
    profession = models.CharField('职业', max_length=255, blank=True)
    area = models.CharField('地区', max_length=255, blank=True)
    company = models.CharField('经纪公司', max_length=255, blank=True)
    school = models.CharField('毕业学校', max_length=255, blank=True)
    intro = models.TextField('简介', blank=True)
    achievement = models.TextField('个人成就', blank=True)
    viewnum = models.IntegerField('浏览', blank=True)
    supportnum = models.IntegerField('支持', blank=True)
    againstnum = models.IntegerField('反对', blank=True)
    createtime = models.DateTimeField('创建时间', blank=True, null=True)
    updatetime = models.DateTimeField('更新时间', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'crawler_star_info'
        verbose_name = '明星信息'
        verbose_name_plural = '明星信息'

    def get_time_string(self):
        return self.createtime.strftime("%Y-%m-%d %H:%M:%S")

    def get_achievement(self):
        return self.achievement.split(';')

class CrawlerStarRelation(models.Model):
    id = models.IntegerField(primary_key=True)
    srcid = models.ForeignKey('CrawlerStarInfo', db_column='srcid', on_delete=models.CASCADE)
    relation_id = models.CharField('人物ID', max_length=255)
    relationship = models.CharField('关系', max_length=255)
    name = models.CharField('姓名', max_length=255)
    portraitpath = models.CharField('头像路径', max_length=255)
    createtime = models.DateTimeField('创建时间', blank=True, null=True)
    updatetime = models.DateTimeField('更新时间', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'crawler_star_relation'
        verbose_name = '明星关系'
        verbose_name_plural = '明星关系'

class CrawlerStarImg(models.Model):
    id = models.IntegerField(primary_key=True)
    srcid = models.ForeignKey('CrawlerStarInfo', db_column='srcid', on_delete=models.CASCADE)
    imgid = models.CharField('图片ID', max_length=255)
    imglink = models.CharField('图片链接', max_length=255)
    imgpath = models.CharField('图片路径', max_length=255)
    portraitid = models.CharField('头像ID', max_length=255)
    portraitlink = models.CharField('头像链接', max_length=255)
    portraitpath = models.CharField('头像路径', max_length=255)
    createtime = models.DateTimeField('创建时间', blank=True, null=True)
    updatetime = models.DateTimeField('更新时间', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'crawler_star_img'
        verbose_name = '明星图片'
        verbose_name_plural = '明星图片'

class CrawlerStarComment(models.Model):
    id = models.IntegerField(primary_key=True)
    srcid = models.ForeignKey('CrawlerStarInfo', db_column='srcid', on_delete=models.CASCADE)
    comment = models.TextField('评论内容', blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='用户')
    supportnum = models.IntegerField('支持', blank=True)
    createtime = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'crawler_book_comment'
        verbose_name = '电影评论'
        verbose_name_plural = '电影评论'

