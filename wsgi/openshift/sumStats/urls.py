from django.conf.urls import patterns, url
from sumStats import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/result/$', views.result, name='result'),
    url(r'^genBar/$', views.genBar, name='genBar'),                   
)
