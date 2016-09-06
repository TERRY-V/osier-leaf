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
from .models import CrawlerBookInfo, CrawlerBookBuy, CrawlerBookImg, CrawlerBookComment

@register.filter(name='mod_lookup')
def mod_lookup(num, val):
    return num % val

def index(request):
    site_info = Website.objects.first()
    column_list = Column.objects.order_by('column_order')
    column_now = Column.objects.get(pk=5)

    book_list = CrawlerBookInfo.objects.order_by('-createtime')[:1000]
    hottest_list = CrawlerBookInfo.objects.order_by('-supportnum')[:10]

    paginator = Paginator(book_list, 20)
    try:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)

    page_range = list(paginator.page_range)[0:5]

    context = {'site_info': site_info, 
            'column_list': column_list,
            'column_now': column_now,
            'book_list': books,
            'query_num': len(book_list),
            'page_range': page_range,
            'hottest_list': hottest_list,}
    return render(request, 'book/index.html', context)

def search(request):
    site_info = Website.objects.first()
    column_list = Column.objects.order_by('column_order')
    column_now = Column.objects.get(pk=5)

    book_list = CrawlerBookInfo.objects.all()
    query = request.GET.get('q')
    if query and len(query):
        book_list = book_list.filter(bookname__contains=query.encode('utf-8'))

    sort = request.GET.get('sort')
    if sort == '1':
    	book_list = book_list.order_by('-createtime')[:1000]
    elif sort == '2':
    	book_list = book_list.order_by('-viewnum')[:1000]
    elif sort == '3':
    	book_list = book_list.order_by('-supportnum')[:1000]
    else:
        sort = '1'
    	book_list = book_list.order_by('-createtime')[:1000]

    page = request.GET.get('page', 1)
    paginator = Paginator(book_list, 20)
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)

    page_num = int(page)
    if page_num >= 5:
        page_range = list(paginator.page_range)[page_num-5:page_num+4]
    else:
        page_range = list(paginator.page_range)[0:page_num+4]

    hottest_list = CrawlerBookInfo.objects.order_by('-supportnum')[:10]

    context = {'site_info': site_info,
            'column_list': column_list,
            'column_now': column_now,
            'query': query,
            'sort': int(sort),
            'query_num': len(book_list),
            'book_list': books,
            'page_range': page_range,
            'hottest_list': hottest_list,}
    return render(request, 'book/search.html', context)

def detail(request, book_id):
    site_info = Website.objects.first()
    column_list = Column.objects.order_by('column_order')
    column_now = Column.objects.get(pk=5)

    book = get_object_or_404(CrawlerBookInfo, srcid=str(book_id))
    book.viewnum += 1
    book.save()

    hottest_comment_list = []
    latest_comment_list = book.crawlerbookcomment_set.order_by('-createtime')
    if len(latest_comment_list) > 30:
        hottest_comment_list = book.crawlerbookcomment_set.order_by('-supportnum')[:5]

    hottest_list = CrawlerBookInfo.objects.order_by('-supportnum')[:10]

    context = {'site_info': site_info, 
            'column_list': column_list, 
            'column_now': column_now,
            'book': book,
            'hottest_comment_list': hottest_comment_list,
            'latest_comment_list': latest_comment_list,
            'hottest_list': hottest_list,}
    return render(request, 'book/detail.html', context)

def vote(request, book_id):
    article_type = request.POST.get("type")

    book = get_object_or_404(CrawlerBookInfo, srcid=str(book_id))

    response = {}
    response['status'] = 0

    if article_type == '1':
        book.supportnum += 1
        book.save()

        response['message'] = 'ok'
        response['supportnum'] = book.supportnum
        response['againstnum'] = book.againstnum
    elif article_type == '2':
        book.againstnum += 1
        book.save()

        response['message'] = 'ok'
        response['supportnum'] = book.supportnum
        response['againstnum'] = book.againstnum
    else:
        response['status'] = -1
        response['message'] = 'param type error!'

    return HttpResponse (
        json.dumps(response),
        content_type="application/json"
    )

def comment(request, book_id):
    comment = request.POST.get("comment")
    user = request.user

    if not user.is_authenticated():
        return HttpResponse("亲，你还没有登录哦！", status=403)

    if not comment:
        return HttpResponse("请输入评论内容！", status=403)

    if len(comment.strip())<5:
        return HttpResponse("评论内容内容过短！", status=403)

    book_comment = CrawlerBookComment()
    book_comment.srcid = CrawlerBookInfo.objects.get(srcid=str(book_id))
    book_comment.comment = comment
    book_comment.user = user
    book_comment.supportnum = 0
    book_comment.againstnum = 0
    book_comment.save()

    context = {'latest': book_comment,}
    return render(request, "book/latest_comment.html", context)

def support(request, book_id):
    cid = request.POST.get("cid")

    comment = get_object_or_404(CrawlerBookComment, id=cid)

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

