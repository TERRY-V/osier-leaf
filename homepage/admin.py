from django.contrib import admin

from .models import Website, Column, News, FriendLinks

@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'site_slogan', 'site_author', 'site_description')
    list_display_links = ('site_name',)

@admin.register(Column)
class ColumnAdmin(admin.ModelAdmin):
    list_display = ('column_name', 'column_url', 'column_icon', 'column_order', 'column_status')
    list_display_links = ('column_name',)

@admin.register(FriendLinks)
class FriendLinksAdmin(admin.ModelAdmin):
    list_display = ('linkname', 'linkurl', 'linkorder', 'formatCreateTime')
    list_display_links = ('linkname',)

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('news_time', 'news_title', 'formatCreateTime')
    list_display_links = ('news_time', 'news_title',)

