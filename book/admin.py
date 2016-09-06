# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import CrawlerBookInfo

# Register your models here.

@admin.register(CrawlerBookInfo)
class CrawlerBookInfoAdmin(admin.ModelAdmin):
    fieldsets = [
            ('采集链接信息',       {'fields': ['srcid', 'website', 'srclink', 'type', 'extratype', 'createtime']}),
            ('电影基本信息',       {'fields': ['bookname', 'subtitle', 'originname', 'author', 'translator', 'press', 'year', 'page', 'price', 'collection', 'bidding', 'isbn']}),
            ('电影重要信息',       {'fields': ['score', 'content_intro', 'author_intro', 'dir', 'reviewlink']}),
            ]
    list_display = ('srcid', 'bookname', 'author', 'press')
    list_display_links = ('bookname',)
    list_filter = ['type', 'extratype']
    list_per_page = 20
    readonly_fields = ('srcid', 'bookname', 'createtime')
    search_fields = ['bookname']

