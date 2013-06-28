#coding:utf-8
#blog urls
from django.conf.urls import patterns, include, url
import django.contrib.auth
import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pycms.views.home', name='home'),
    # url(r'^pycms/', include('pycms.foo.urls')),
    url(r'^$',views.home),
    url(r'^login/$',views.login_view),
    url(r'^about/$',views.about),
    url(r'^contactme/$',views.contact),
    url(r'^test/$',views.test),
    url(r'^logout/$',views.logout_view)
    #url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'blog/login/login.html'}),
)
