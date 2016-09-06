# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import CrawlerFoodMaterialInfo

# Register your models here.

@admin.register(CrawlerFoodMaterialInfo)
class CrawlerFoodMaterialInfoAdmin(admin.ModelAdmin):
    fieldsets = [
            ('采集链接信息',       {'fields': ['srcid', 'website', 'srclink', 'type', 'extratype', 'createtime']}),
            ('食材基本信息',       {'fields': ['name', 'alias', 'calory', 'classify']}),
            ('食材重要信息',       {'fields': ['suitable_people', 'introduce', 'component', 'effect', 'nutrition', 'operation', 'selection', 'storage']}),
            ]
    list_display = ('srcid', 'name', 'alias', 'classify')
    list_display_links = ('name',)
    list_filter = ['type', 'extratype']
    list_per_page = 20
    readonly_fields = ('srcid', 'name', 'createtime')
    search_fields = ['name']

