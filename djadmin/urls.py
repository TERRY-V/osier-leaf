from django.conf.urls import url
from djadmin.views import DjadminCenter

from . import views

urlpatterns = [
        url(r'^login$', views.login, name="login"),
        url(r'^main$', views.main, name="main"),
        url(r'^setting$', views.setting, name="setting"),
        url(r'^menu$', views.menu, name="menu"),
        url(r'^menu/add$', views.addMenu, name="addMenu"),
        url(r'^menu/(?P<menu_id>[0-9]+)/change$', views.changeMenu, name='changeMenu'),
        url(r'^menu/(?P<menu_id>[0-9]+)/delete$', views.deleteMenu, name='deleteMenu'),
        url(r'^user$', views.user, name="user"),
        url(r'^user/add$', views.addUser, name="addUser"),
        url(r'^user/(?P<user_id>[0-9]+)/change$', views.changeUser, name='changeUser'),
        url(r'^(?P<slug>\w+)check$', DjadminCenter.as_view()),
        ]

