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
from .models import CrawlerShoppingInfo

def search(request):
    site_info = Website.objects.first()
    column_list = Column.objects.order_by('column_order')
    column_now = Column.objects.get(pk=9)

    shopping_list = CrawlerShoppingInfo.objects.all()
    query = request.GET.get('q')
    if query and len(query):
        shopping_list = shopping_list.filter(name__contains=query.encode('utf-8'))
    elif query is None:
        query = ''

    sort = request.GET.get('sort')
    if sort == '1':
    	shopping_list = shopping_list.order_by('-createtime')[:1000]
    elif sort == '2':
    	shopping_list = shopping_list.order_by('-viewnum')[:1000]
    elif sort == '3':
    	shopping_list = shopping_list.order_by('-supportnum')[:1000]
    else:
        sort = '1'
    	shopping_list = shopping_list.order_by('-createtime')[:1000]

    page = request.GET.get('page', 1)
    paginator = Paginator(shopping_list, 20)
    try:
        shoppings = paginator.page(page)
    except PageNotAnInteger:
        shoppings = paginator.page(1)
    except EmptyPage:
        shoppings = paginator.page(paginator.num_pages)

    page_num = int(page)
    if page_num >= 5:
        page_range = list(paginator.page_range)[page_num-5:page_num+4]
    else:
        page_range = list(paginator.page_range)[0:page_num+4]

    context = {'site_info': site_info, 
            'column_list': column_list, 
            'column_now': column_now,
            'query': query,
            'sort': int(sort),
            'query_num': len(shopping_list),
            'shopping_list': shoppings,
            'page_range': page_range}
    return render(request, 'shopping/search.html', context)

