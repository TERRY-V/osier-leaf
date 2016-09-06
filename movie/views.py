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
from .models import CrawlerMovieInfo, CrawlerMoviePlaylink, CrawlerMovieImg, CrawlerMovieComment

@register.filter(name='mod_lookup')
def mod_lookup(num, val):
    return num % val

def index(request):
    site_info = Website.objects.first()
    column_list = Column.objects.order_by('column_order')
    column_now = Column.objects.get(pk=4)

    movie_list = CrawlerMovieInfo.objects.filter(id__lt=29719).order_by('-createtime')[:1000]
    hottest_list = CrawlerMovieInfo.objects.order_by('-score')[:10]

    paginator = Paginator(movie_list, 20)
    try:
        movies = paginator.page(1)
    except EmptyPage:
        movies = paginator.page(paginator.num_pages)

    page_range = list(paginator.page_range)[0:5]

    context = {'site_info': site_info, 
            'column_list': column_list,
            'column_now': column_now,
            'movie_list': movies,
            'query_num': len(movie_list),
            'page_range': page_range,
            'hottest_list': hottest_list,}
    return render(request, 'movie/index.html', context)

def search(request):
    site_info = Website.objects.first()
    column_list = Column.objects.order_by('column_order')
    column_now = Column.objects.get(pk=4)

    movie_list = CrawlerMovieInfo.objects.filter(id__lt=29719)
    query = request.GET.get('q')
    if query and len(query):
        movie_list = movie_list.filter(moviename__contains=query.encode('utf-8'))

    movietype = request.GET.get('type')
    if movietype and len(movietype):
        movie_list = movie_list.filter(movietype__contains=movietype.encode('utf-8'))

    star = request.GET.get('star')
    if star and len(star):
        movie_list = movie_list.filter(starring__contains=star.encode('utf-8'))

    sort = request.GET.get('sort')
    if sort == '1':
    	movie_list = movie_list.order_by('-createtime')[:1000]
    elif sort == '2':
    	movie_list = movie_list.order_by('-viewnum')[:1000]
    elif sort == '3':
    	movie_list = movie_list.order_by('-score')[:1000]
    else:
        sort = '1'
    	movie_list = movie_list.order_by('-createtime')[:1000]

    page = request.GET.get('page', 1)
    paginator = Paginator(movie_list, 20)
    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        movies = paginator.page(1)
    except EmptyPage:
        movies = paginator.page(paginator.num_pages)

    page_num = int(page)
    if page_num >= 5:
        page_range = list(paginator.page_range)[page_num-5:page_num+4]
    else:
        page_range = list(paginator.page_range)[0:page_num+4]

    hottest_list = CrawlerMovieInfo.objects.order_by('-viewnum')[:10]

    context = {'site_info': site_info, 
            'column_list': column_list, 
            'column_now': column_now,
            'query': query,
            'sort': int(sort),
            'query_num': len(movie_list),
            'movie_list': movies,
            'page_range': page_range,
            'hottest_list': hottest_list,}
    return render(request, 'movie/search.html', context)

def detail(request, movie_id):
    site_info = Website.objects.first()
    column_list = Column.objects.order_by('column_order')
    column_now = Column.objects.get(pk=4)

    movie = get_object_or_404(CrawlerMovieInfo, srcid=str(movie_id))
    movie.viewnum += 1
    movie.save()

    hottest_comment_list = []
    latest_comment_list = movie.crawlermoviecomment_set.order_by('-createtime')
    if len(latest_comment_list) > 30:
        hottest_comment_list = movie.crawlermoviecomment_set.order_by('-supportnum')[:5]

    hottest_list = CrawlerMovieInfo.objects.order_by('-viewnum')[:10]

    context = {'site_info': site_info, 
            'column_list': column_list, 
            'column_now': column_now,
            'movie': movie,
            'hottest_comment_list': hottest_comment_list,
            'latest_comment_list': latest_comment_list,
            'hottest_list': hottest_list,}
    return render(request, 'movie/detail.html', context)

def vote(request, movie_id):
    article_type = request.POST.get("type")

    movie = get_object_or_404(CrawlerMovieInfo, srcid=str(movie_id))

    response = {}
    response['status'] = 0

    if article_type == '1':
        movie.supportnum += 1
        movie.save()

        response['message'] = 'ok'
        response['supportnum'] = movie.supportnum
        response['againstnum'] = movie.againstnum
    elif article_type == '2':
        movie.againstnum += 1
        movie.save()

        response['message'] = 'ok'
        response['supportnum'] = movie.supportnum
        response['againstnum'] = movie.againstnum
    else:
        response['status'] = -1
        response['message'] = 'param type error!'

    return HttpResponse (
        json.dumps(response),
        content_type="application/json"
    )

def comment(request, movie_id):
    comment = request.POST.get("comment")
    user = request.user

    if not user.is_authenticated():
        return HttpResponse("亲，你还没有登录哦！", status=403)

    if not comment:
        return HttpResponse("请输入评论内容！", status=403)

    if len(comment.strip())<5:
        return HttpResponse("评论内容内容过短！", status=403)

    movie_comment = CrawlerMovieComment()
    movie_comment.srcid = CrawlerMovieInfo.objects.get(srcid=str(movie_id))
    movie_comment.comment = comment
    movie_comment.user = user
    movie_comment.supportnum = 0
    movie_comment.againstnum = 0
    movie_comment.save()

    context = {'latest': movie_comment,}
    return render(request, "movie/latest_comment.html", context)

def support(request, movie_id):
    cid = request.POST.get("cid")

    comment = get_object_or_404(CrawlerMovieComment, id=cid)

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

