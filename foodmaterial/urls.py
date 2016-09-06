from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^(?P<foodmaterial_id>[0-9]+)/$', views.detail, name='detail'),
        url(r'^search/$', views.search, name='search'),
        url(r'^(?P<foodmaterial_id>[0-9]+)/vote/$', views.vote, name='vote'),
        ]
