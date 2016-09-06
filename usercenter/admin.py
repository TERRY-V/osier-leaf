# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin

from .models import User
from .forms import UserCreationForm

# Register your models here.

class PynxlUserAdmin(UserAdmin):
    add_form = UserCreationForm

    add_fieldsets = (
            (None, {
                'classes': ('wide',),
                'fields': ('username', 'email', 'password1', 'password2')
                }),
            )

    fieldsets = (
            (u'基本信息', {'fields': ('username', 'password', 'email')}),
            (u'权限', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
            (u'时间信息', {'fields': ('last_login', 'date_joined')}),
            )

admin.site.unregister(Group)
admin.site.register(User, PynxlUserAdmin)

