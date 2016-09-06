# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import CrawlerMovieInfo

# Register your models here.

@admin.register(CrawlerMovieInfo)
class CrawlerMovieInfoAdmin(admin.ModelAdmin):
    fieldsets = [
            ('采集链接信息',       {'fields': ['srcid', 'website', 'srclink', 'type', 'extratype', 'createtime']}),
            ('电影基本信息',       {'fields': ['moviename', 'starring', 'language', 'area', 'director', 'movietype', 'writer', 'release_company', 'release_time', 'manufacture_company', 'alias']}),
            ('电影重要信息',       {'fields': ['score', 'story']}),
            ]
    list_display = ('srcid', 'moviename', 'movietype', 'starring')
    list_display_links = ('moviename',)
    list_filter = ['type', 'extratype']
    list_per_page = 20
    readonly_fields = ('srcid', 'moviename', 'createtime')
    search_fields = ['moviename']

