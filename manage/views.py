#coding:utf-8
#views of manage
import re
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import (authenticate, login ,logout)
from django.template import RequestContext
from blog.models import BasicSettings,Tags,ThreadTypes,Posts,Status
from django.db import transaction
#own import 
from pycms import settings
from manage.forms import MakePostForm
from blog.data import UserInfo,BasicInfo

static_root = settings.GLOBA_STATIC_URL
blog_login_url = settings.BLOG_ROOT_URL+'login/'

#公用的添加一个图片自动等比例缩放的js的函数，适合于字符串
def new_post(mkp_form, request, id=None,):
    """make a new post form a makepost form in web page,return a Posts object."""
    newpost = Posts()
    newpost.init()
    newpost.authorid = int(request.user.id)
    newpost.title = mkp_form.cleaned_data['title']
    newpost.name = mkp_form.cleaned_data['short_title']     #缩略名
    newpost.cover = mkp_form.cleaned_data['cover_url']
    newpost.introduction = mkp_form.cleaned_data['introduction']
    newpost.content = js_resize_img(mkp_form.cleaned_data['content'])
    newpost.status = Status.objects.get(id=2)        #id为2是已发布的文章，默认为已发布，后面再改
    tagids = mkp_form.cleaned_data['tags']
    if len(tagids) != 0:
        for tagid in tagids:
            tagid = str(tagid)
            tag = Tags.objects.get(id=tagid)
            newpost.post_tagid.add(tag)
    threadtypeid = mkp_form.cleaned_data['threadtypeid']
    newpost.threadtypeid = ThreadTypes.objects.get(id=threadtypeid)
    if mkp_form.cleaned_data['commentnotshow'] != '':
        newpost.comment_status = False
    else:
        newpost.comment_status = True
    return newpost
    
    
def js_resize_img(text):
    """返回一串在<img />标签中被添加了一段自动调整显示大小的js引用的文本对象"""
    bold = re.compile(r'(<img.+?)/>')
    return bold.sub(r'\1 onload="javascript:DrawImage(this,600,600)" />',text)
    
@login_required(login_url=blog_login_url)
def home(request):
    #static_root = settings.GLOBA_STATIC_URL
    return render_to_response('manage/base.html',{'static_root':static_root})

@login_required(login_url=blog_login_url)
@transaction.commit_on_success
def make_post(request):
    """make post page.It generate the make_post page and receive 
    data form the page then store them into database."""
    basic_info = BasicInfo(request)
    #get方法，显示表单页面
    if request.method == 'GET':
        mkp_form = MakePostForm()
        return render_to_response('manage/make_post.html',locals(),context_instance=RequestContext(request))
    #post方法提交表单并跳转
    if request.method == 'POST':
        mkp_form = MakePostForm(request.POST)
        #Posts.objects.get(id='1')
        if mkp_form.is_valid():
            newpost = new_post(mkp_form,request)
            newpost.save()
            return HttpResponse('all done')
        else:
            return render_to_response('manage/make_post.html',locals(),context_instance=RequestContext(request))
#修改文章
@login_required(login_url=blog_login_url)        
def modify_post(request):
    basic_info = BasicInfo(request)
    #get方法，显示表单页面
    if request.method == 'GET':
        mkp_form = ModifyPostForm()
        return render_to_response('manage/modify_post.html',locals(),context_instance=RequestContext(request))
    #post方法提交表单并跳转
    if request.method == 'POST':
        mkp_form = MakePostForm(request.POST)
        #Posts.objects.get(id='1')
        if mkp_form.is_valid():
            newpost = new_post(mkp_form,request)
            newpost.save()
            return HttpResponse('all done')
        else:
            return render_to_response('manage/modify_post.html',locals(),context_instance=RequestContext(request))
            
        