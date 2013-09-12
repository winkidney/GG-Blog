#coding:utf-8
#views of manage
import re
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import (authenticate, login ,logout)
from django.template import RequestContext
from blog.models import BasicSettings,Tags,ThreadTypes,Posts,Status
#own import 
from pycms import settings

static_root = settings.GLOBA_STATIC_URL
blog_login_url = settings.BLOG_ROOT_URL+'login/'

#公用的添加一个图片自动等比例缩放的js的函数，适合于字符串
def js_resize_img(text):
    """返回一串在<img />标签中被添加了一段自动调整显示大小的js引用的文本对象"""
    bold = re.compile(r'(<img.+?)/>')
    return bold.sub(r'\1 onload="javascript:DrawImage(this,600,600)" />',text)
    
@login_required(login_url=blog_login_url)
def home(request):
    #static_root = settings.GLOBA_STATIC_URL
    return render_to_response('manage/base.html',{'static_root':static_root})

@login_required(login_url=blog_login_url)
def make_post(request):
    #get方法，显示表单页面
    if request.method == 'GET':
        #标签
        tags = Tags.objects.all()
        #分类
        threadtypes = ThreadTypes.objects.all()
        return render_to_response('manage/make_post.html',{'static_root':static_root,'tags':tags,'threadtypes':threadtypes},context_instance=RequestContext(request))
    #post方法提交表单并跳转
    if request.method == 'POST':
        newpost = Posts() #Posts.objects.get(id='1')
        
        #检查项目是否为空
        checklist = []
        checklist.append(request.POST.get('title'))
        checklist.append(request.POST.get('short_title'))
        checklist.append(request.POST.get('cover_url'))
        checklist.append(request.POST.get('summarise'))
        checklist.append(request.POST.get('content'))
        if '' not in checklist:
            newpost.init()
            newpost.post_authorid = int(request.user.id)
            newpost.post_title = request.POST.get('title')
            newpost.post_name = request.POST.get('short_title')     #缩略名
            newpost.post_cover = request.POST.get('cover_url')
            newpost.post_introduction = request.POST.get('summarise')
            newpost.post_content = js_resize_img(request.POST.get('content'))
            newpost.post_status = Status.objects.get(id='2')        #id为2是已发布的文章，默认为已发布，后面再改
            tagids = request.POST.getlist('tag')
            if tagids != '':
                for tagid in tagids:
                    tagid = str(tagid)
                    tag = Tags.objects.get(id=tagid)
                    newpost.post_tagid.add(tag)
            threadtypeid = str(request.POST.get('threadtype'))
            newpost.post_threadtypeid = ThreadTypes.objects.get(id=threadtypeid)
            if request.POST.get('commentnotshow') != '':
                newpost.comment_status = False
            else:
                newpost.comment_status = True
            newpost.save()
            return HttpResponse('all done')
        else:
            #清理之前生成的newpost对象，因为init方法将newpost写入了数据库
            #newpost.delete()
            return HttpResponse('fail')
#修改文章
@login_required(login_url=blog_login_url)        
def modify_post(request):
    #get方法，显示表单页面
    if request.method == 'GET':
        #标签
        tags = Tags.objects.all()
        #分类
        threadtypes = ThreadTypes.objects.all()
        return render_to_response('manage/make_post.html',{'static_root':static_root,'tags':tags,'threadtypes':threadtypes},context_instance=RequestContext(request))
    #post方法提交表单并跳转
    if request.method == 'POST':
        newpost = Posts() #Posts.objects.get(id='1')
        
        #检查项目是否为空
        checklist = []
        checklist.append(request.POST.get('title'))
        checklist.append(request.POST.get('short_title'))
        checklist.append(request.POST.get('cover_url'))
        checklist.append(request.POST.get('summarise'))
        checklist.append(request.POST.get('content'))
        if '' not in checklist:
            #如果数据没有错误，则调用init（）方法初始化数据库（其中包含一个写入数据库的过程）
            newpost.init()
            newpost.post_authorid = int(request.user.id)
            newpost.post_title = request.POST.get('title')
            newpost.post_name = request.POST.get('short_title')     #缩略名
            newpost.post_cover = request.POST.get('cover_url')
            newpost.post_introduction = request.POST.get('summarise')
            newpost.post_content = request.POST.get('content')
            newpost.post_status = Status.objects.get(id='2')        #id为2是已发布的文章，默认为已发布，后面再改
            tagids = request.POST.getlist('tag')
            if tagids != '':
                for tagid in tagids:
                    tagid = str(tagid)
                    tag = Tags.objects.get(id=tagid)
                    newpost.post_tagid.add(tag)
            threadtypeid = str(request.POST.get('threadtype'))
            newpost.post_threadtypeid = ThreadTypes.objects.get(id=threadtypeid)
            if request.POST.get('commentnotshow') != '':
                newpost.comment_status = False
            else:
                newpost.comment_status = True
            newpost.save()
            return HttpResponse('all done')
        else:
            #newpost.delete()
            return HttpResponse('fail')
            
        