# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import CrawlerHealthInfo, CrawlerHealthArticle

class CrawlerHealthArticleInline(admin.StackedInline):
    model = CrawlerHealthArticle
    extra = 0

@admin.register(CrawlerHealthInfo)
class CrawlerMovieInfoAdmin(admin.ModelAdmin):
    fieldsets = [
            ('采集链接信息',       {'fields': ['srcid', 'website', 'srclink', 'type', 'extratype', 'createtime']}),
            ('健康基本信息',       {'fields': ['title', 'summary']}),
            ]
    list_display = ('srcid', 'title')
    list_display_links = ('title',)
    list_filter = ['type', 'extratype']
    list_per_page = 20
    readonly_fields = ('srcid', 'createtime')
    search_fields = ['title']
    inlines = [CrawlerHealthArticleInline]

