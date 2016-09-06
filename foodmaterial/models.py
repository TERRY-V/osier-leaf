# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from datetime import datetime
from django.db import models

# Create your models here.

class CrawlerFoodMaterialInfo(models.Model):
    id = models.IntegerField('食材编号', primary_key=True)
    website = models.CharField('网站来源', max_length=255, blank=True)
    srcid = models.IntegerField('采集编号', blank=True, null=True)
    srclink = models.CharField('采集URL', max_length=255, blank=True)
    type = models.IntegerField('一级分类', blank=True, null=True)
    extratype = models.IntegerField('二级分类', blank=True, null=True)
    name = models.CharField('食材名称', max_length=255, blank=True)
    alias = models.CharField('食材别名', max_length=255, blank=True)
    calory = models.CharField('食材能量', max_length=255, blank=True)
    classify = models.CharField('食材分类', max_length=255, blank=True)
    suitable_people = models.TextField('适用人群', blank=True)
    introduce = models.TextField('食材的介绍', blank=True)
    component = models.TextField('食材的营养成分', blank=True)
    effect = models.TextField('食材的使用效果', blank=True)
    nutrition = models.TextField('食材的营养价值', blank=True)
    operation = models.TextField('食材的做法', blank=True)
    selection = models.TextField('挑选方法', blank=True)
    storage = models.TextField('储存方法', blank=True)
    viewnum = models.IntegerField('浏览', blank=True)
    supportnum = models.IntegerField('支持', blank=True)
    againstnum = models.IntegerField('反对', blank=True)
    createtime = models.DateTimeField('创建时间', blank=True, null=True)
    updatetime = models.DateTimeField('更新时间', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'crawler_food_material_info'
        verbose_name = '食材信息'
        verbose_name_plural = '食材信息'

    def labels_as_list(self):
        return self.alias.split('、')

    def get_time_string(self):
        return self.createtime.strftime("%Y-%m-%d %H:%M:%S")

