import django.contrib.auth.views
from django.conf.urls import url
from django.contrib.auth import views as auth_views

urlpatterns = [
    # url(r'^$', views.index, name='index'),
    url(r'^login/$', auth_views.login,
        {'template_name': 'cabinet/login.html'}, name='login'),
    url(
        r'^logout/$', django.contrib.auth.views.logout,
        {'next_page': '/'}
    ),
]
