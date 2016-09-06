from django.conf.urls import url
from usercenter.views import UserCenter

from . import views

urlpatterns = [
        url(r'^refreshcaptcha$', views.refreshCaptcha, name="refreshCaptcha"),
        url(r'^login$', views.login, name="login"),
        url(r'^register$', views.register, name="register"),
        url(r'^forgetpassword$', views.forgetPassword, name="forgetPassword"),
        url(r'^changeavatar$', views.changeAvatar, name="changeAvatar"),
        url(r'^changepassword$', views.changePassword, name="changePassword"),
        url(r'^resetpassword/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', views.resetPassword, name="resetPassword"),
        url(r'^(?P<slug>\w+)check$', UserCenter.as_view()),
        ]
