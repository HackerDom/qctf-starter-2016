from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<clar_id>\d+)/$', views.read_clar, name='read_clar'),
]
