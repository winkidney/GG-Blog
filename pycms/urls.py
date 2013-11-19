#coding:utf-8
#urls of pycms
from pycms import settings,views
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
    #url(r'^$',views.home_view),
    #static files
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    #url(r'^blog/admin/', include(admin.site.urls)),
    #my own
    url(r'^$', include('blog.urls')),
    #上传文件处理(ueditor)
    url(r'^ueditor_imgup/$','pycms.views.ueditor_img_up'),
    url(r'^ueditor_fileup/$','pycms.views.ueditor_file_up'),
    url(r'^ueditor_scrawlup/$','pycms.views.ueditor_scraw_up'),
        #modifiedurl
    url(r'^ueditor_getRemoteImage/$','pycms.views.ueditor_getRemoteImage'),
    url(r'^ueditor_getMovie/$','pycms.views.ueditor_getMovie'),
    url(r'^ueditor_imageManager/$','pycms.views.ueditor_imageManager'),
        #url(r'^ueditor_getremoteimg/$','pycms.views.ueditor_img_manager'),
        #url(r'^ueditor_getmovie/$','pycms.views.ueditor_get_movie'),
        #url(r'^ueditor_imagemanager/$','pycms.views.ue_get_remote_img')
)
urlpatterns += staticfiles_urlpatterns()
#handler404 = 'mysite.views.my_custom_404_view'
