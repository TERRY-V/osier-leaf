from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'pynxl.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^', include('homepage.urls')),
    url(r'^foodmaterial/', include('foodmaterial.urls')),
    url(r'^cookbook/', include('cookbook.urls')),
    url(r'^movie/', include('movie.urls')),
    url(r'^book/', include('book.urls')),
    url(r'^image/', include('image.urls')),
    url(r'^star/', include('star.urls')),
    url(r'^health/', include('health.urls')),
    url(r'^shopping/', include('shopping.urls')),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^usercenter/', include('usercenter.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^djadmin/', include('djadmin.urls')),
]

