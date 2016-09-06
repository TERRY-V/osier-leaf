# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import json
import urllib2

from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.defaulttags import register

from django import template
from django.utils import timezone
from django.views.generic import View, TemplateView, ListView, DetailView

from homepage.models import Website, Column
from .models import CrawlerHealthInfo, CrawlerHealthArticle

@register.filter(name='mod_lookup')
def mod_lookup(num, val):
    return num % val

def index(request):
    site_info = Website.objects.first()
    column_list = Column.objects.order_by('column_order')
    column_now = Column.objects.get(pk=8)

    health_list = CrawlerHealthInfo.objects.order_by('-createtime')[:1000]
    hottest_list = CrawlerHealthInfo.objects.order_by('-viewnum')[:10]

    paginator = Paginator(health_list, 20)
    try:
        healths = paginator.page(1)
    except EmptyPage:
        healths = paginator.page(paginator.num_pages)

    page_range = list(paginator.page_range)[0:5]

    context = {'site_info': site_info, 
            'column_list': column_list,
            'column_now': column_now,
            'health_list': healths,
            'query_num': len(health_list),
            'page_range': page_range,
            'hottest_list': hottest_list,}
    return render(request, 'health/index.html', context)

def search(request):
    site_info = Website.objects.first()
    column_list = Column.objects.order_by('column_order')
    column_now = Column.objects.get(pk=8)

    health_list = CrawlerHealthInfo.objects.all()
    query = request.GET.get('q')
    if query and len(query):
        health_list = health_list.filter(title__contains=query.encode('utf-8'))

    sort = request.GET.get('sort')
    if sort == '1':
    	health_list = health_list.order_by('-createtime')[:1000]
    elif sort == '2':
    	health_list = health_list.order_by('-viewnum')[:1000]
    elif sort == '3':
    	health_list = health_list.order_by('-supportnum')[:1000]
    else:
        sort = '1'
    	health_list = health_list.order_by('-createtime')[:1000]

    page = request.GET.get('page', 1)
    paginator = Paginator(health_list, 20)
    try:
        healths = paginator.page(page)
    except PageNotAnInteger:
        healths = paginator.page(1)
    except EmptyPage:
        healths = paginator.page(paginator.num_pages)

    page_num = int(page)
    if page_num >= 5:
        page_range = list(paginator.page_range)[page_num-5:page_num+4]
    else:
        page_range = list(paginator.page_range)[0:page_num+4]

    hottest_list = CrawlerHealthInfo.objects.order_by('-viewnum')[:10]

    context = {'site_info': site_info, 
            'column_list': column_list, 
            'column_now': column_now,
            'query': query,
            'sort': int(sort),
            'query_num': len(health_list),
            'health_list': healths,
            'page_range': page_range,
            'hottest_list': hottest_list,}
    return render(request, 'health/search.html', context)

def detail(request, health_id):
    site_info = Website.objects.first()
    column_list = Column.objects.order_by('column_order')
    column_now = Column.objects.get(pk=8)

    health = get_object_or_404(CrawlerHealthInfo, srcid=str(health_id))
    health.viewnum += 1
    health.save()

    hottest_comment_list = []
    latest_comment_list = health.crawlerhealthcomment_set.order_by('-createtime')
    if len(latest_comment_list) > 30:
        hottest_comment_list = health.crawlerhealthcomment_set.order_by('-supportnum')[:5]

    hottest_list = CrawlerHealthInfo.objects.order_by('-viewnum')[:10]

    context = {'site_info': site_info, 
            'column_list': column_list, 
            'column_now': column_now,
            'health': health,
            'hottest_comment_list': hottest_comment_list,
            'latest_comment_list': latest_comment_list,
            'hottest_list': hottest_list,}
    return render(request, 'health/detail.html', context)

def vote(request, health_id):
    article_type = request.POST.get("type")

    health = get_object_or_404(CrawlerHealthInfo, srcid=str(health_id))

    response = {}
    response['status'] = 0

    if article_type == '1':
        health.supportnum += 1
        health.save()

        response['message'] = 'ok'
        response['supportnum'] = health.supportnum
        response['againstnum'] = health.againstnum
    elif article_type == '2':
        health.againstnum += 1
        health.save()

        response['message'] = 'ok'
        response['supportnum'] = health.supportnum
        response['againstnum'] = health.againstnum
    else:
        response['status'] = -1
        response['message'] = 'param type error!'

    return HttpResponse (
        json.dumps(response),
        content_type="application/json"
    )

def comment(request, health_id):
    comment = request.POST.get("comment")
    user = request.user

    if not user.is_authenticated():
        return HttpResponse("亲，你还没有登录哦！", status=403)

    if not comment:
        return HttpResponse("请输入评论内容！", status=403)

    if len(comment.strip())<5:
        return HttpResponse("评论内容内容过短！", status=403)

    health_comment = CrawlerHealthComment()
    health_comment.srcid = CrawlerHealthInfo.objects.get(srcid=str(health_id))
    health_comment.comment = comment
    health_comment.user = user
    health_comment.supportnum = 0
    health_comment.againstnum = 0
    health_comment.save()

    context = {'latest': health_comment,}
    return render(request, "health/latest_comment.html", context)

def support(request, health_id):
    cid = request.POST.get("cid")

    comment = get_object_or_404(CrawlerHealthComment, id=cid)

    response = {}
    response['status'] = 0

    comment.supportnum += 1
    comment.save()

    response['message'] = 'ok'
    response['supportnum'] = comment.supportnum

    return HttpResponse (
        json.dumps(response),
        content_type="application/json"
    )

