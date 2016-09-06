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
from .models import CrawlerStarInfo, CrawlerStarRelation, CrawlerStarImg, CrawlerStarComment

@register.filter(name='mod_lookup')
def mod_lookup(num, val):
    return num % val

def index(request):
    site_info = Website.objects.first()
    column_list = Column.objects.order_by('column_order')
    column_now = Column.objects.get(pk=7)

    star_list = CrawlerStarInfo.objects.order_by('-viewnum')[:1000]
    hottest_list = CrawlerStarInfo.objects.order_by('-supportnum')[:10]

    paginator = Paginator(star_list, 20)
    try:
        stars = paginator.page(1)
    except EmptyPage:
        stars = paginator.page(paginator.num_pages)

    page_range = list(paginator.page_range)[0:5]

    context = {'site_info': site_info, 
            'column_list': column_list,
            'column_now': column_now,
            'star_list': stars,
            'query_num': len(star_list),
            'page_range': page_range,
            'hottest_list': hottest_list,}
    return render(request, 'star/index.html', context)

def search(request):
    site_info = Website.objects.first()
    column_list = Column.objects.order_by('column_order')
    column_now = Column.objects.get(pk=7)

    star_list = CrawlerStarInfo.objects.all()
    query = request.GET.get('q')
    if query and len(query):
        star_list = star_list.filter(name__contains=query.encode('utf-8'))

    sort = request.GET.get('sort')
    if sort == '1':
    	star_list = star_list.order_by('-createtime')[:1000]
    elif sort == '2':
    	star_list = star_list.order_by('-viewnum')[:1000]
    elif sort == '3':
    	star_list = star_list.order_by('-supportnum')[:1000]
    else:
        sort = '1'
    	star_list = star_list.order_by('-createtime')[:1000]

    page = request.GET.get('page', 1)
    paginator = Paginator(star_list, 20)
    try:
        stars = paginator.page(page)
    except PageNotAnInteger:
        stars = paginator.page(1)
    except EmptyPage:
        stars = paginator.page(paginator.num_pages)

    page_num = int(page)
    if page_num >= 5:
        page_range = list(paginator.page_range)[page_num-5:page_num+4]
    else:
        page_range = list(paginator.page_range)[0:page_num+4]

    hottest_list = CrawlerStarInfo.objects.order_by('-supportnum')[:10]

    context = {'site_info': site_info,
            'column_list': column_list,
            'column_now': column_now,
            'query': query,
            'sort': int(sort),
            'query_num': len(star_list),
            'star_list': stars,
            'page_range': page_range,
            'hottest_list': hottest_list,}
    return render(request, 'star/search.html', context)

def detail(request, star_id):
    site_info = Website.objects.first()
    column_list = Column.objects.order_by('column_order')
    column_now = Column.objects.get(pk=7)

    star = get_object_or_404(CrawlerStarInfo, srcid=str(star_id))
    star.viewnum += 1
    star.save()

    hottest_comment_list = []
    latest_comment_list = star.crawlerstarcomment_set.order_by('-createtime')
    if len(latest_comment_list) > 30:
        hottest_comment_list = star.crawlerstarcomment_set.order_by('-supportnum')[:5]

    hottest_list = CrawlerStarInfo.objects.order_by('-supportnum')[:10]

    context = {'site_info': site_info, 
            'column_list': column_list, 
            'column_now': column_now,
            'star': star,
            'hottest_comment_list': hottest_comment_list,
            'latest_comment_list': latest_comment_list,
            'hottest_list': hottest_list,}
    return render(request, 'star/detail.html', context)

def vote(request, star_id):
    article_type = request.POST.get("type")

    star = get_object_or_404(CrawlerStarInfo, srcid=str(star_id))

    response = {}
    response['status'] = 0

    if article_type == '1':
        star.supportnum += 1
        star.save()

        response['message'] = 'ok'
        response['supportnum'] = star.supportnum
        response['againstnum'] = star.againstnum
    elif article_type == '2':
        star.againstnum += 1
        star.save()

        response['message'] = 'ok'
        response['supportnum'] = star.supportnum
        response['againstnum'] = star.againstnum
    else:
        response['status'] = -1
        response['message'] = 'param type error!'

    return HttpResponse (
        json.dumps(response),
        content_type="application/json"
    )

def comment(request, star_id):
    comment = request.POST.get("comment")
    user = request.user

    if not user.is_authenticated():
        return HttpResponse("亲，你还没有登录哦！", status=403)

    if not comment:
        return HttpResponse("请输入评论内容！", status=403)

    if len(comment.strip())<5:
        return HttpResponse("评论内容内容过短！", status=403)

    star_comment = CrawlerStarComment()
    star_comment.srcid = CrawlerStarInfo.objects.get(srcid=str(star_id))
    star_comment.comment = comment
    star_comment.user = user
    star_comment.supportnum = 0
    star_comment.againstnum = 0
    star_comment.save()

    context = {'latest': star_comment,}
    return render(request, "star/latest_comment.html", context)

def support(request, star_id):
    cid = request.POST.get("cid")

    comment = get_object_or_404(CrawlerStarComment, id=cid)

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

