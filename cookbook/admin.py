# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import CrawlerCookbookInfo

# Register your models here.

@admin.register(CrawlerCookbookInfo)
class CrawlerCookbookInfoAdmin(admin.ModelAdmin):
    fieldsets = [
            ('采集链接信息',       {'fields': ['srcid', 'website', 'srclink', 'type', 'extratype', 'createtime']}),
            ('美食基本信息',       {'fields': ['name', 'main_spice', 'assist_spice', 'cooks', 'classify']}),
            ('美食重要信息',       {'fields': ['comment', 'trick']}),
            ]
    list_display = ('srcid', 'name', 'cooks', 'classify')
    list_display_links = ('name',)
    list_filter = ['type', 'extratype']
    list_per_page = 20
    readonly_fields = ('srcid', 'name', 'createtime')
    search_fields = ['name']

