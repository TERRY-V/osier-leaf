# -*- coding: utf-8 -*-

import base64
import smtplib

from django.conf import settings
from django import forms
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from email.header import Header
from email.mime.text import MIMEText

from captcha.fields import CaptchaField

from usercenter.models import User

class UserCreationForm(forms.ModelForm):

    error_messages = {
        'duplicate_username': "该用户名已存在.",
        'password_mismatch': "两次密码不一致.",
        'duplicate_email': '该Email已经存在.'
    }

    username = forms.RegexField(
        min_length = 5,
        max_length = 30,
        regex = r'^[\w.@+-]+$',
        error_messages = {
            'invalid':  "用户名只能包含字母、数字和字符@/./+/-/_",
            'required': "用户名不能为空"
        }
    )

    email = forms.EmailField(
        error_messages = {
            'invalid':  "Email格式错误",
            'required': 'Email不能为空'
            }
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput,
        error_messages = {
            'required': "密码不能为空"
            }
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput,
        error_messages = {
            'required': "确认密码不能为空"
        }
    )

    class Meta:
        model = User
        fields = ("username", "email")

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages["duplicate_username"]
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                    self.error_messages["password_mismatch"]
            )
        return password2

    def clean_email(self):
        email = self.cleaned_data["email"]

        try:
            User._default_manager.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(
            self.error_messages["duplicate_email"]
        )

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class PasswordForgetForm(forms.Form):

    error_messages = {
        'email_error': "用户名不存在或用户名与Email不相符",
        'captcha_error': "验证码错误",
    }

    username = forms.RegexField(
        min_length = 5,
        max_length = 30,
        regex = r'^[\w.@+-]+$',
        error_messages = {
            'invalid': "用户名只能包含字母、数字和字符@/./+/-/_",
            'required': "用户名不能为空"}
        )

    email = forms.EmailField(
        error_messages = {
            'invalid':  "Email格式错误",
            'required': 'Email不能为空'}
    )

    key = forms.RegexField(
        regex = r'^.*$',
        error_messages = {
            'required': '验证码不能为空'}
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if username and email:
            try:
                self.user = User.objects.get(
                    username=username, email=email, is_active=True
                )
            except User.DoesNotExist:
                raise forms.ValidationError(self.error_messages["email_error"])

        return self.cleaned_data

    def save(self, from_email=None, request=None, token_generator=default_token_generator):
        email = self.cleaned_data['email']
        current_site = get_current_site(request)
        site_name = current_site.name
        domain = current_site.domain
        uid = base64.urlsafe_b64encode(force_bytes(self.user.pk)).rstrip(b'\n=')

        token = token_generator.make_token(self.user)
        protocol = 'http'

        title = "{} 密码重置".format(site_name)
        content = "".join([
            "亲，您收到这封邮件是因为你请求重置你在网站 {} 的账户密码\n\n".format(
                site_name
            ),
            "请访问该页面并输入新密码:\n\n",
            "{}://{}/usercenter/resetpassword/{}/{}/\n\n".format(
                protocol, domain, uid, token
            ),
            "您的用户名: {}\n\n".format(
                self.user.username
            ),
            "感谢使用我们的站点!\n\n",
            "{} 团队\n\n\n".format(site_name)
        ])

        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(settings.MAIL_HOST, 25)
            smtpObj.login(settings.MAIL_USER, settings.MAIL_PASSWORD)

            message = MIMEText(content, 'plain', 'utf-8')
            message['Subject'] = Header(title, 'utf-8')
            smtpObj.sendmail(settings.MAIL_USER, [self.user.email], message.as_string())
        except smtplib.SMTPException:
            print 'Error: 邮件发送失败!'

