# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import CrawlerShoppingInfo, CrawlerShoppingType

@admin.register(CrawlerShoppingType)
class CrawlerShoppingTypeAdmin(admin.ModelAdmin):
    fieldsets = [
            ('商品分类信息',       {'fields': ['name', 'pid']})
            ]
    list_display = ('id', 'name', 'pid', 'formatCreateTime')
    list_display_links = ('name',)
    list_filter = []
    list_per_page = 20
    search_fields = ['name']

@admin.register(CrawlerShoppingInfo)
class CrawlerShoppingInfoAdmin(admin.ModelAdmin):
    fieldsets = [
            ('商品链接信息',       {'fields': ['srcid', 'website']}),
            ('商品基本信息',       {'fields': ['name', 'srclink', 'imglink', 'shoppingtype', 'price', 'starttime', 'finishtime']})
            ]
    list_display = ('id', 'srcid', 'name', 'shoppingtype', 'price', 'formatCreateTime')
    list_display_links = ('name',)
    list_filter = []
    list_per_page = 20
    search_fields = ['name']

