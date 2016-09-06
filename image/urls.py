from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^search/$', views.search, name='search'),
        url(r'^getitem/$', views.getItem, name='getItem'),
        url(r'^(?P<img_id>[0-9]+)/$', views.detail, name='detail'),
        ]
