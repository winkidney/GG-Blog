#coding:utf-8
#urls of manage
from django.conf.urls import patterns, include, url
import views
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pycms.views.home', name='home'),
    # url(r'^pycms/', include('pycms.foo.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^$',views.home_view),
    url(r'^makepost/$',views.make_post_view),
    url(r'^edit/(?P<article_id>\d{1,10})/$',views.modify_post_view),
    
)