#coding:utf-8
#blog urls
from django.conf.urls import patterns, include, url
import django.contrib.auth
import views
#some private settings
articles_path = r'' 

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pycms.views.home', name='home'),
    # url(r'^pycms/', include('pycms.foo.urls')),
    url(r'^$',views.home_view),
    url(r'^page/(?P<pagenum>\d{1,4})/',views.home_view),
    url(r'^login/$',views.login_view),
    url(r'^about/$',views.about_view),
    url(r'^contactme/$',views.contact_view),
    url(r'^logout/$',views.logout_view),
    url(r'^manage/', include('manage.urls')),
    #阅读文章url，文章数量限制为1000,000,000。
    url(r'^articles/(?P<article_id>\d{1,10})/$',views.articles_view),
    url(r'^articles/$',views.archives_view),
    url(r'^archives/$',views.archives_index_view),
    url(r'^archives/(?P<year>\d{4})/(?P<month>\d{1,2})/$',views.archives_view),
    url(r'^tags/(?P<tagname>.{1,20})/$',views.tags_view),
    url(r'^test/$',views.test_view),
    #url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'blog/login/login.html'}),
    #tiny mce
    #url(r'^tinymce/',include('tinymce.urls')),
)
