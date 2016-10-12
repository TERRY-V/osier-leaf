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
from django.views.generic import View, TemplateView, ListView, DetailView

from .models import Website, Column, News
from cookbook.models import CrawlerCookbookInfo
from foodmaterial.models import CrawlerFoodMaterialInfo
from movie.models import CrawlerMovieInfo
from book.models import CrawlerBookInfo

def index(request):
    site_info = Website.objects.first()
    column_now = Column.objects.get(pk=3)
    column_list = Column.objects.order_by('column_order')

    newest_cookbook_list = CrawlerCookbookInfo.objects.order_by('-createtime')[:9]
    support_cookbook_list = CrawlerCookbookInfo.objects.order_by('-supportnum')[:8]
    hottest_movie_list = CrawlerMovieInfo.objects.filter(id__lt=29719).order_by('-viewnum')[:8]
    support_movie_list = CrawlerMovieInfo.objects.filter(id__lt=29719).order_by('-supportnum')[:8]
    hottest_book_list = CrawlerBookInfo.objects.order_by('-viewnum')[:8]
    support_book_list = CrawlerBookInfo.objects.order_by('-supportnum')[:8]

    context = {'site_info': site_info, 
            'column_now': column_now,
            'column_list': column_list,
            'newest_cookbook_list': newest_cookbook_list,
            'support_cookbook_list': support_cookbook_list,
            'hottest_movie_list': hottest_movie_list,
            'support_movie_list': support_movie_list,
            'hottest_book_list': hottest_book_list,
            'support_book_list': support_book_list,}
    return render(request, 'homepage/index.html', context)

def introduce(request):
    site_info = Website.objects.first()
    column_now = Column.objects.get(pk=3)
    column_list = Column.objects.order_by('column_order')

    context = {'site_info': site_info, 
            'column_now': column_now,
            'column_list': column_list,}
    return render(request, 'homepage/introduce.html', context)

def trends(request):
    site_info = Website.objects.first()
    column_now = Column.objects.get(pk=3)
    column_list = Column.objects.order_by('column_order')
    news_list = News.objects.order_by('-createtime')

    context = {'site_info': site_info, 
            'column_now': column_now,
            'column_list': column_list,
            'news_list': news_list}
    return render(request, 'homepage/trends.html', context)

def contactus(request):
    site_info = Website.objects.first()
    column_now = Column.objects.get(pk=3)
    column_list = Column.objects.order_by('column_order')

    context = {'site_info': site_info, 
            'column_now': column_now,
            'column_list': column_list,}
    return render(request, 'homepage/contactus.html', context)

def declaration(request):
    site_info = Website.objects.first()
    column_now = Column.objects.get(pk=3)
    column_list = Column.objects.order_by('column_order')

    context = {'site_info': site_info, 
            'column_now': column_now,
            'column_list': column_list,}
    return render(request, 'homepage/declaration.html', context)

def help(request):
    site_info = Website.objects.first()
    column_now = Column.objects.get(pk=3)
    column_list = Column.objects.order_by('column_order')

    context = {'site_info': site_info, 
            'column_now': column_now,
            'column_list': column_list,}
    return render(request, 'homepage/help.html', context)

def links(request):
    site_info = Website.objects.first()
    column_now = Column.objects.get(pk=3)
    column_list = Column.objects.order_by('column_order')

    context = {'site_info': site_info, 
            'column_now': column_now,
            'column_list': column_list,}
    return render(request, 'homepage/links.html', context)

def mobile(request):
    site_info = Website.objects.first()
    column_now = Column.objects.get(pk=3)
    column_list = Column.objects.order_by('column_order')

    context = {'site_info': site_info, 
            'column_now': column_now,
            'column_list': column_list,}
    return render(request, 'homepage/mobile.html', context)

def advertisement(request):
    site_info = Website.objects.first()
    column_now = Column.objects.get(pk=3)
    column_list = Column.objects.order_by('column_order')

    context = {'site_info': site_info, 
            'column_now': column_now,
            'column_list': column_list,}
    return render(request, 'homepage/advertisement.html', context)

