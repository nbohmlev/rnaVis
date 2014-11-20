from django.conf.urls import patterns, url
from sumStats import views
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    url(r'^$', login_required(views.index), name='index'),
    url(r'^(?P<pk>\d+)/$', login_required(views.DetailView.as_view()), name='detail'),
    url(r'^(?P<pk>\d+)/result/$', login_required(views.result), name='result'),
    url(r'^genBar/$', login_required(views.genBar), name='genBar'),                   
)
