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
from .models import CrawlerFoodMaterialInfo

@register.filter(name='mod_lookup')
def mod_lookup(num, val):
    return num % val

def index(request):
    site_info = Website.objects.first()
    column_list = Column.objects.order_by('column_order')
    column_now = Column.objects.get(pk=1)

    food_material_list = CrawlerFoodMaterialInfo.objects.order_by('-createtime')[:1000]
    hottest_list = CrawlerFoodMaterialInfo.objects.order_by('-viewnum')[:10]

    page = request.GET.get('page')
    paginator = Paginator(food_material_list, 20)
    try:
        food_materials = paginator.page(1)
    except EmptyPage:
        food_materials = paginator.page(paginator.num_pages)

    page_range = list(paginator.page_range)[0:5]

    context = {'site_info': site_info, 
            'column_now': column_now,
            'column_list': column_list, 
            'food_material_list': food_materials,
            'query_num': len(food_material_list),
            'page_range': page_range,
            'hottest_list': hottest_list,}
    return render(request, 'foodmaterial/index.html', context)

def search(request):
    site_info = Website.objects.first()
    column_now = Column.objects.get(pk=1)
    column_list = Column.objects.order_by('column_order')

    food_material_list = CrawlerFoodMaterialInfo.objects.all()
    query = request.GET.get('q')
    if query and len(query):
        food_material_list = CrawlerFoodMaterialInfo.objects.filter(name__contains=query.encode('utf-8'))

    sort = request.GET.get('sort')
    if sort == '1':
    	food_material_list = food_material_list.order_by('-createtime')[:1000]
    elif sort == '2':
    	food_material_list = food_material_list.order_by('-viewnum')[:1000]
    elif sort == '3':
    	food_material_list = food_material_list.order_by('-supportnum')[:1000]
    else:
        sort = '1'
    	food_material_list = food_material_list.order_by('-createtime')[:1000]

    page = request.GET.get('page', 1)
    paginator = Paginator(food_material_list, 25)
    try:
        food_materials = paginator.page(page)
    except PageNotAnInteger:
        food_materials = paginator.page(1)
    except EmptyPage:
        food_materials = paginator.page(paginator.num_pages)

    page_num = int(page)
    if page_num >= 5:
        page_range = list(paginator.page_range)[page_num-5:page_num+4]
    else:
        page_range = list(paginator.page_range)[0:page_num+4]

    hottest_list = CrawlerFoodMaterialInfo.objects.order_by('-viewnum')[:10]

    context = {'site_info': site_info, 
            'column_now': column_now,
            'column_list': column_list, 
            'food_material_list': food_materials,
            'page_range': page_range,
            'query': query,
            'sort': int(sort),
            'query_num': len(food_material_list),
            'hottest_list': hottest_list,}
    return render(request, 'foodmaterial/search.html', context)

def detail(request, foodmaterial_id):
    site_info = Website.objects.first()
    column_now = Column.objects.get(pk=1)
    column_list = Column.objects.order_by('column_order')

    food_material = get_object_or_404(CrawlerFoodMaterialInfo, srcid=str(foodmaterial_id))
    food_material.viewnum += 1
    food_material.save()

    hottest_list = CrawlerFoodMaterialInfo.objects.order_by('-viewnum')[:10]

    context = {'site_info': site_info, 
            'column_now': column_now,
            'column_list': column_list, 
            'food_material': food_material, 
            'hottest_list': hottest_list,}
    return render(request, 'foodmaterial/detail.html', context)

def vote(request, foodmaterial_id):
    article_type = request.POST.get("type")

    food_material = get_object_or_404(CrawlerFoodMaterialInfo, srcid=str(foodmaterial_id))

    response = {}
    response['status'] = 0

    if article_type == '1':
        food_material.supportnum += 1
        food_material.save()

        response['message'] = 'ok'
        response['supportnum'] = food_material.supportnum
        response['againstnum'] = food_material.againstnum
    elif article_type == '2':
        food_material.againstnum += 1
        food_material.save()

        response['message'] = 'ok'
        response['supportnum'] = food_material.supportnum
        response['againstnum'] = food_material.againstnum
    else:
        response['status'] = -1
        response['message'] = 'param type error!'

    return HttpResponse (
        json.dumps(response),
        content_type="application/json"
    )

