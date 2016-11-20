from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^scoreboard/$', views.scoreboard, name='scoreboard'),
    url(r'^hints/$', views.hints, name='hints'),
    url(r'^check_flag/(?P<task_id>\d+)/$', views.check_flag,
        name='check_flag'),
    url(r'^hints/(?P<hint_id>\d+)/buy/$', views.buy_hint,
        name='buy_hint'),
]
