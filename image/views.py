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
from .models import CrawlerImageInfo, CrawlerImageCategory

@register.filter(name='mod_lookup')
def mod_lookup(num, val):
    return num % val

def index(request):
    site_info = Website.objects.first()
    column_list = Column.objects.order_by('column_order')
    column_now = Column.objects.get(pk=6)

    type = 1
    extratype = 1

    type_list = CrawlerImageCategory.objects.filter(pid=0)
    extratype_list = CrawlerImageCategory.objects.filter(pid=type)

    context = {'site_info': site_info,
            'column_list': column_list,
            'column_now': column_now,
            'type': type,
            'extratype': extratype,
            'type_list': type_list,
            'extratype_list': extratype_list,}
    return render(request, 'image/index.html', context)

def search(request):
    site_info = Website.objects.first()
    column_list = Column.objects.order_by('column_order')
    column_now = Column.objects.get(pk=6)
    
    type_list = CrawlerImageCategory.objects.filter(pid=0)

    query = request.GET.get('q').encode('utf-8')
    type = request.GET.get('type')
    if type == None:
        type = ''
        extratype_list = CrawlerImageCategory.objects.filter(pid=1)
    else:
        type = int(type)
        extratype_list = CrawlerImageCategory.objects.filter(pid=type)

    extratype = request.GET.get('extratype')
    if extratype == None:
        extratype = ''
    else:
        extratype = int(extratype)

    context = {'site_info': site_info,
            'column_list': column_list,
            'column_now': column_now,
            'type': type,
            'extratype': extratype,
            'query': query,
            'type_list': type_list,
            'extratype_list': extratype_list,}
    return render(request, 'image/search.html', context)

def getItem(request):
    image_list = CrawlerImageInfo.objects.all()

    query = request.GET.get('q')
    if query:
        image_list = image_list.filter(title__contains=query.encode('utf-8'))

    type = request.GET.get('type')
    if type:
        image_list = image_list.filter(type=type)

    extratype = request.GET.get('extratype')
    if extratype:
        image_list = image_list.filter(extratype=extratype)

    image_list = image_list[:1000]

    page = request.GET.get('page', 1)
    paginator = Paginator(image_list, 10)
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        images = []

    items = []
    for image in images:
        item = {}
        item['imgid'] = image.imgid
        item['title'] = image.title
        item['imgpath'] = image.imgpath
        item['imgsize'] = image.imgsize
        items.append(item)

    image_dict = {"status": 0, "images": items}
    return HttpResponse(json.dumps(image_dict), content_type="application/json")

def detail(request, img_id):
    site_info = Website.objects.first()
    column_list = Column.objects.order_by('column_order')
    column_now = Column.objects.get(pk=6)

    image = get_object_or_404(CrawlerImageInfo, imgid=str(img_id))

    context = {'site_info': site_info, 
            'column_list': column_list, 
            'column_now': column_now, 
            'image': image,}
    return render(request, 'image/detail.html', context)

