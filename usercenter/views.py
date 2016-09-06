# -*- coding: utf-8 -*-

import os
import json

from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views.generic import View
from django.core.mail import send_mail
from django.core.exceptions import PermissionDenied
from django.contrib import auth
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import (base36_to_int, is_safe_url, urlsafe_base64_decode, urlsafe_base64_encode)

from homepage.models import Website, Column
from usercenter.forms import UserCreationForm, PasswordForgetForm
from usercenter.models import User

from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url

class UserCenter(View):

    def post(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug')

        if slug == 'login':
            return self.login(request)
        elif slug == "register":
            return self.register(request)
        elif slug == "logout":
            return self.logout(request)
        elif slug == "forgetpassword":
            return self.forgetPassword(request)
        elif slug == "changepassword":
            return self.changePassword(request)
        elif slug == "resetpassword":
            return self.resetPassword(request)
        elif slug == "changeavatar":
            return self.changeavatar(request)

        raise PermissionDenied

    def verify_captcha(self, key, hashkey):
        captcha_key = CaptchaStore.objects.filter(hashkey=hashkey)[0].response
        if key.lower() == captcha_key:
            return True
        return False

    def login(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        key = request.POST.get("key")
        hashkey = request.POST.get("hashkey")

        errors = []
        if self.verify_captcha(key, hashkey):
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
            else:
                errors.append("用户名或密码不正确")
        else:
            errors.append("验证码错误")
        return HttpResponse(json.dumps({"errors": errors}), content_type="application/json")

    def register(self, request):
        username = request.POST.get("username")
        password2 = request.POST.get("password2")
        key = request.POST.get("key")
        hashkey = request.POST.get("hashkey")

        form = UserCreationForm(request.POST)
        errors = []

        if form.is_valid():
            if self.verify_captcha(key, hashkey):
                new_user = form.save()
                user = auth.authenticate(username=username, password=password2)
                auth.login(request, user)
            else:
                errors.append("验证码错误")
        else:
            for k, v in form.errors.items():
                errors.append(v.as_text())
        return HttpResponse(json.dumps({"errors": errors}), content_type="application/json")

    def logout(self, request):
        if not request.user.is_authenticated():
            raise PermissionDenied

        auth.logout(request)
        return HttpResponse('OK')

    def forgetPassword(self, request):
        key = request.POST.get("key")
        hashkey = request.POST.get("hashkey")

        form = PasswordForgetForm(request.POST)
        errors = []

        if form.is_valid():
            if not self.verify_captcha(key, hashkey):
                errors.append("验证码错误")
            else:
                opts = {
                        'token_generator': default_token_generator,
                        'from_email': None,
                        'request': request,
                }
                user = form.save(**opts)
        else:
            for k, v in form.errors.items():
                errors.append(v.as_text())
        return HttpResponse(json.dumps({"errors": errors}), content_type="application/json")

    def changePassword(self, request):
        if not request.user.is_authenticated():
            raise PermissionDenied

        form = PasswordChangeForm(request.user, request.POST)
        errors = []

        if form.is_valid():
            user = form.save()
            auth.logout(request)
        else:
            for k, v in form.errors.items():
                errors.append(v.as_text())
        return HttpResponse(json.dumps({"errors": errors}), content_type="application/json")

    def resetPassword(self, request):
        uidb64 = request.POST.get("uidb64")
        token = request.POST.get("token")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        token_generator = default_token_generator

        if user is not None and token_generator.check_token(user, token):
            form = SetPasswordForm(user, request.POST)
            errors = []

            if form.is_valid():
                user = form.save()
            else:
                for k, v in form.errors.items():
                    errors.append(v.as_text())

            return HttpResponse(json.dumps({"errors": errors}), content_type="application/json")
        else:
            return HttpResponse("密码重置链接已失效，重设密码失败！", status=403)

def refreshCaptcha(request):
    resp = dict()
    resp["status"] = 0
    resp["captcha_key"] = CaptchaStore.generate_key()
    resp["captcha_hashkey"] = captcha_image_url(resp["captcha_key"])
    return HttpResponse(json.dumps(resp), content_type='application/json')

def login(request):
    site_info = Website.objects.first()
    column_list = Column.objects.order_by('column_order')

    context = {'site_info': site_info, 
            'column_list': column_list,}
    return render(request, 'usercenter/login.html', context)

def register(request):
    site_info = Website.objects.first()
    column_list = Column.objects.order_by('column_order')

    context = {'site_info': site_info, 
            'column_list': column_list,}
    return render(request, 'usercenter/register.html', context)

def changeAvatar(request):
    site_info = Website.objects.first()
    column_list = Column.objects.order_by('column_order')

    if not request.user.is_authenticated():
        raise PermissionDenied

    context = {'site_info': site_info, 
            'column_list': column_list,}
    return render(request, 'usercenter/changeavatar.html', context)

def changePassword(request):
    site_info = Website.objects.first()
    column_list = Column.objects.order_by('column_order')

    if not request.user.is_authenticated():
        raise PermissionDenied

    context = {'site_info': site_info, 
            'column_list': column_list,}
    return render(request, 'usercenter/changepassword.html', context)

def forgetPassword(request):
    site_info = Website.objects.first()
    column_list = Column.objects.order_by('column_order')
    
    context = {'site_info': site_info, 
            'column_list': column_list,}
    return render(request, 'usercenter/forgetpassword.html', context)

def resetPassword(request, uidb64, token):
    site_info = Website.objects.first()
    column_list = Column.objects.order_by('column_order')

    context = {'site_info': site_info, 
            'column_list': column_list,
            'uidb64': uidb64,
            'token': token,}
    return render(request, 'usercenter/resetpassword.html', context)

