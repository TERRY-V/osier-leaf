# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import CrawlerStarInfo, CrawlerStarRelation

class CrawlerStarRelationInline(admin.StackedInline):
    model = CrawlerStarRelation
    extra = 0

@admin.register(CrawlerStarInfo)
class CrawlerStarInfoAdmin(admin.ModelAdmin):
    fieldsets = [
            ('采集链接信息',       {'fields': ['srcid', 'website', 'srclink', 'type', 'extratype', 'createtime']}),
            ('明星基本信息',       {'fields': ['name', 'engname', 'aliase', 'gender', 'birthday', 'profession', 'area', 'company', 'school']}),
            ('明星重要信息',       {'fields': ['intro', 'achievement']}),
            ]
    list_display = ('srcid', 'name', 'gender')
    list_display_links = ('name',)
    list_filter = ['type', 'extratype']
    list_per_page = 20
    readonly_fields = ('srcid', 'name', 'createtime')
    search_fields = ['name']
    inlines = [CrawlerStarRelationInline]

