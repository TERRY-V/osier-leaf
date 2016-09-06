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
from .models import CrawlerCookbookInfo, CrawlerCookbookStep, CrawlerCookbookImg, CrawlerCookbookComment

@register.filter(name='mod_lookup')
def mod_lookup(num, val):
    return num % val

def index(request):
    site_info = Website.objects.first()
    column_list = Column.objects.order_by('column_order')
    column_now = Column.objects.get(pk=2)

    cookbook_list = CrawlerCookbookInfo.objects.order_by('-createtime')[:1000]
    hottest_list = CrawlerCookbookInfo.objects.order_by('-viewnum')[:10]

    paginator = Paginator(cookbook_list, 20)
    try:
        cookbooks = paginator.page(1)
    except EmptyPage:
        cookbooks = paginator.page(paginator.num_pages)

    page_range = list(paginator.page_range)[0:5]

    context = {'site_info': site_info, 
            'column_list': column_list,
            'column_now': column_now,
            'cookbook_list': cookbooks,
            'query_num': len(cookbook_list),
            'page_range': page_range,
            'hottest_list': hottest_list,}
    return render(request, 'cookbook/index.html', context)

def search(request):
    site_info = Website.objects.first()
    column_list = Column.objects.order_by('column_order')
    column_now = Column.objects.get(pk=2)

    cookbook_list = CrawlerCookbookInfo.objects.all()
    query = request.GET.get('q')
    if query and len(query):
        cookbook_list = cookbook_list.filter(name__contains=query.encode('utf-8'))

    tag = request.GET.get('tag')
    if tag and len(tag):
        cookbook_list = cookbook_list.filter(classify__contains=tag.encode('utf-8'))

    sort = request.GET.get('sort')
    if sort == '1':
    	cookbook_list = cookbook_list.order_by('-createtime')[:1000]
    elif sort == '2':
    	cookbook_list = cookbook_list.order_by('-viewnum')[:1000]
    elif sort == '3':
    	cookbook_list = cookbook_list.order_by('-supportnum')[:1000]
    else:
        sort = '1'
    	cookbook_list = cookbook_list.order_by('-createtime')[:1000]

    page = request.GET.get('page', 1)
    paginator = Paginator(cookbook_list, 20)
    try:
        cookbooks = paginator.page(page)
    except PageNotAnInteger:
        cookbooks = paginator.page(1)
    except EmptyPage:
        cookbooks = paginator.page(paginator.num_pages)

    page_num = int(page)
    if page_num >= 5:
        page_range = list(paginator.page_range)[page_num-5:page_num+4]
    else:
        page_range = list(paginator.page_range)[0:page_num+4]

    hottest_list = CrawlerCookbookInfo.objects.order_by('-viewnum')[:10]

    context = {'site_info': site_info, 
            'column_list': column_list, 
            'column_now': column_now,
            'query': query,
            'sort': int(sort),
            'query_num': len(cookbook_list),
            'cookbook_list': cookbooks,
            'page_range': page_range,
            'hottest_list': hottest_list,}
    return render(request, 'cookbook/search.html', context)

def detail(request, cookbook_id):
    site_info = Website.objects.first()
    column_list = Column.objects.order_by('column_order')
    column_now = Column.objects.get(pk=2)

    cookbook = get_object_or_404(CrawlerCookbookInfo, srcid=str(cookbook_id))
    cookbook.viewnum += 1
    cookbook.save()

    hottest_comment_list = []
    latest_comment_list = cookbook.crawlercookbookcomment_set.order_by('-createtime')
    if len(latest_comment_list) > 30:
        hottest_comment_list = cookbook.crawlercookbookcomment_set.order_by('-supportnum')[:5]

    hottest_list = CrawlerCookbookInfo.objects.order_by('-viewnum')[:10]

    context = {'site_info': site_info, 
            'column_list': column_list, 
            'column_now': column_now,
            'cookbook': cookbook,
            'hottest_comment_list': hottest_comment_list,
            'latest_comment_list': latest_comment_list,
            'hottest_list': hottest_list,}
    return render(request, 'cookbook/detail.html', context)

def vote(request, cookbook_id):
    article_type = request.POST.get("type")

    cookbook = get_object_or_404(CrawlerCookbookInfo, srcid=str(cookbook_id))

    response = {}
    response['status'] = 0

    if article_type == '1':
        cookbook.supportnum += 1
        cookbook.save()

        response['message'] = 'ok'
        response['supportnum'] = cookbook.supportnum
        response['againstnum'] = cookbook.againstnum
    elif article_type == '2':
        cookbook.againstnum += 1
        cookbook.save()

        response['message'] = 'ok'
        response['supportnum'] = cookbook.supportnum
        response['againstnum'] = cookbook.againstnum
    else:
        response['status'] = -1
        response['message'] = 'param type error!'

    return HttpResponse (
        json.dumps(response),
        content_type="application/json"
    )

def comment(request, cookbook_id):
    comment = request.POST.get("comment")
    user = request.user

    if not user.is_authenticated():
        return HttpResponse("亲，你还没有登录哦！", status=403)

    if not comment:
        return HttpResponse("请输入评论内容！", status=403)

    if len(comment.strip())<5:
        return HttpResponse("评论内容内容过短！", status=403)

    cookbook_comment = CrawlerCookbookComment()
    cookbook_comment.srcid = CrawlerCookbookInfo.objects.get(srcid=str(cookbook_id))
    cookbook_comment.comment = comment
    cookbook_comment.user = user
    cookbook_comment.supportnum = 0
    cookbook_comment.againstnum = 0
    cookbook_comment.save()

    context = {'latest': cookbook_comment,}
    return render(request, "cookbook/latest_comment.html", context)

def support(request, cookbook_id):
    cid = request.POST.get("cid")

    comment = get_object_or_404(CrawlerCookbookComment, id=cid)

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

