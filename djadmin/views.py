# -*- coding: utf-8 -*-

import os
import json

from django.contrib import auth
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site

from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.http import HttpResponse, Http404

from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render

from django.template.defaulttags import register
from django.utils.http import (base36_to_int, is_safe_url, urlsafe_base64_decode, urlsafe_base64_encode)
from django.views.generic import View

from djadmin.models import SiteInfo, MenuInfo
from usercenter.forms import UserCreationForm

class DjadminCenter(View):

    def post(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug')

        if slug == 'login':
            return self.login(request)
        elif slug == 'logout':
            return self.logout(request)
        raise PermissionDenied

    def login(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")

        context = {"status": 0}
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_staff:
            auth.login(request, user)
        elif user is not None:
            context["status"] = -1
            context["errors"] = []
            context["errors"].append('用户名权限不够！')
        else:
            context["status"] = -1
            context["errors"] = []
            context["errors"].append(u'用户名或密码错误！')
        return HttpResponse(json.dumps(context), content_type="application/json")

    def logout(self, request):
        auth.logout(request)
        return HttpResponse({"status": 0})

def login(request):
    site_info = SiteInfo.objects.first()
    context = {'site_info': site_info}
    return render(request, 'djadmin/login.html', context)

@login_required(login_url='/djadmin/login')
def main(request):
    site_info = SiteInfo.objects.first()
    menu_list = MenuInfo.objects.order_by('menu_order')

    context = {'site_info': site_info, 'menu_list': menu_list}
    return render(request, 'djadmin/main.html', context)

@login_required(login_url='/djadmin/login')
def setting(request):
    site_info = SiteInfo.objects.first()
    menu_list = MenuInfo.objects.order_by('menu_order')
    menu_now = get_object_or_404(MenuInfo, menu_link='/djadmin/setting')

    if request.method == 'POST':
        site_info.site_name = request.POST.get('name')
        site_info.site_slogan = request.POST.get('slogan')
        site_info.site_athor = request.POST.get('author')
        site_info.site_keywords = request.POST.get('keywords')
        site_info.site_description = request.POST.get('description')
        site_info.site_copyright = request.POST.get('copyright')
        site_info.site_license = request.POST.get('license')
        site_info.site_email = request.POST.get('email')
        site_info.site_phone = request.POST.get('phone')
        site_info.save()
        messages.add_message(request, messages.INFO, u'系统设置信息保存成功！')

    context = {'site_info': site_info, 
            'menu_list': menu_list,
            'menu_now': menu_now}
    return render(request, 'djadmin/setting.html', context)

@login_required(login_url='/djadmin/login')
def menu(request):
    site_info = SiteInfo.objects.first()
    menu_list = MenuInfo.objects.order_by('menu_order')
    menu_now = get_object_or_404(MenuInfo, menu_link='/djadmin/menu')

    context = {'site_info': site_info, 
            'menu_list': menu_list,
            'menu_now': menu_now}
    return render(request, 'djadmin/menu.html', context)

@login_required(login_url='/djadmin/login')
def addMenu(request):
    site_info = SiteInfo.objects.first()
    menu_list = MenuInfo.objects.order_by('menu_order')
    menu_now = get_object_or_404(MenuInfo, menu_link='/djadmin/menu')

    if request.method == 'POST':
        name = request.POST.get('name')
        pid = request.POST.get('pid')
        link = request.POST.get('link')
        order = request.POST.get("order")
        visible = request.POST.get("visible")
        menu = MenuInfo(menu_name=name, menu_pid=pid, menu_link=link, menu_order=order, menu_visible=visible)
        menu.save()
        messages.add_message(request, messages.INFO, u'菜单信息添加成功！')
        return redirect('/djadmin/menu')

    context = {'site_info': site_info, 
            'menu_list': menu_list,
            'menu_now': menu_now}
    return render(request, 'djadmin/addmenu.html', context)

@login_required(login_url='/djadmin/login')
def changeMenu(request, menu_id):
    site_info = SiteInfo.objects.first()
    menu_list = MenuInfo.objects.order_by('menu_order')
    menu_now = get_object_or_404(MenuInfo, menu_link='/djadmin/menu')

    menu = get_object_or_404(MenuInfo, id=menu_id)
    if request.method == 'POST':
        menu.menu_name = request.POST.get('name')
        menu.menu_pid = request.POST.get('pid')
        menu.menu_link = request.POST.get('link')
        menu.menu_order = request.POST.get("order")
        menu.menu_visible = request.POST.get("visible")
        menu.save()
        messages.add_message(request, messages.INFO, u'菜单信息保存成功！')
        return redirect('/djadmin/menu')

    context = {'site_info': site_info, 
            'menu_list': menu_list,
            'menu': menu,
            'menu_now': menu_now}
    return render(request, 'djadmin/changemenu.html', context)

@login_required(login_url='/djadmin/login')
def deleteMenu(request, menu_id):
    site_info = SiteInfo.objects.first()
    menu_list = MenuInfo.objects.order_by('menu_order')
    menu_now = get_object_or_404(MenuInfo, menu_link='/djadmin/menu')

    menu = get_object_or_404(MenuInfo, id=menu_id)
    menu.delete()
    messages.add_message(request, messages.INFO, u'菜单信息删除成功！')
    return redirect('/djadmin/menu')

''' user '''
@login_required(login_url='/djadmin/login')
def user(request):
    site_info = SiteInfo.objects.first()
    menu_list = MenuInfo.objects.order_by('menu_order')
    menu_now = get_object_or_404(MenuInfo, menu_link='/djadmin/user')

    user_list = get_user_model().objects.all()
    keyword = request.GET.get('q')
    if keyword and len(keyword):
        user_list = user_list.filter(username=keyword.encode('utf-8'))

    page = request.GET.get('page', 1)
    paginator = Paginator(user_list, 20)
    try:
        page = int(page)
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = []

    if page >= 5:
        page_range = list(paginator.page_range)[page-5: page+4]
    else:
        page_range = list(paginator.page_range)[0: page+4]

    context = {'site_info': site_info, 
            'menu_list': menu_list,
            'menu_now': menu_now,
            'page_range': page_range,
            'users': users,
            'query_num': len(user_list)}
    return render(request, 'djadmin/user.html', context)

@login_required(login_url='/djadmin/login')
def addUser(request):
    site_info = SiteInfo.objects.first()
    menu_list = MenuInfo.objects.order_by('menu_order')
    menu_now = get_object_or_404(MenuInfo, menu_link='/djadmin/user')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            messages.add_message(request, messages.INFO, u'添加用户成功！')
            return redirect('/djadmin/user')
        else:
            for k, v in form.errors.items():
                messages.add_message(request, messages.INFO, v.as_text())

    context = {'site_info': site_info, 
            'menu_list': menu_list,
            'menu_now': menu_now}
    return render(request, 'djadmin/adduser.html', context)

@login_required(login_url='/djadmin/login')
def changeUser(request, user_id):
    site_info = SiteInfo.objects.first()
    menu_list = MenuInfo.objects.order_by('menu_order')
    menu_now = get_object_or_404(MenuInfo, menu_link='/djadmin/user')

    user = get_object_or_404(get_user_model(), id=user_id)
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            user = form.save()
            messages.add_message(request, messages.INFO, u'用户信息编辑成功！')
            return redirect('/djadmin/user')
        else:
            for k, v in form.errors.items():
                messages.add_message(request, messages.INFO, k + ' ' + v.as_text())

    context = {'site_info': site_info, 
            'menu_list': menu_list,
            'user': user,
            'menu_now': menu_now}
    return render(request, 'djadmin/changeuser.html', context)
