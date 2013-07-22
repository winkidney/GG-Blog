#coding:utf-8
#views of manage
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import (authenticate, login ,logout)
from django.template import RequestContext
from blog.models import BasicSettings,Tags,ThreadTypes
#own import 
from pycms import settings

static_root = settings.GLOBA_STATIC_URL
blog_login_url = settings.BLOG_ROOT_URL+'login/'

@login_required(login_url=blog_login_url)
def home(request):
    #static_root = settings.GLOBA_STATIC_URL
    return render_to_response('manage/base.html',{'static_root':static_root})

@login_required(login_url=blog_login_url)
def make_post(request):
    if request.method == 'GET':
        #标签
        tags = Tags.objects.all()
        #分类
        threadtypes = ThreadTypes.objects.all()
        return render_to_response('manage/make_post.html',{'static_root':static_root,'tags':tags,'threadtypes':threadtypes},context_instance=RequestContext(request))
    if request.method == 'POST':
        apple = request.POST.getlist('tag')
        return HttpResponse('all done')