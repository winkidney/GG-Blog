#coding:utf-8
#urls of pycms
from pycms import settings
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns 
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pycms.views.home', name='home'),
    # url(r'^pycms/', include('pycms.foo.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    #static files
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    #my own
    url(r'^blog/', include('blog.urls')),
    #上传文件处理
    url(r'^ueditor_imgup/$','pycms.views.ueditor_img_up'),
    url(r'^ueditor_fileup/$','pycms.views.ueditor_file_up'),
    
)
urlpatterns += staticfiles_urlpatterns()
