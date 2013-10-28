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
    url(r'^logout/$',views.logout_view),
    url(r'^manage/', include('manage.urls')),
    #阅读文章url，文章数量限制为1000,000,000。
    url(r'^articles/(\d{1,10})/$',views.articles_view),
    url(r'^archives/(\d{4})/(\d{1,2})/',views.archives_view)
    #url(r'^test/$',views.TagsCreate),
    #url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'blog/login/login.html'}),
    #tiny mce
    #url(r'^tinymce/',include('tinymce.urls')),
)
