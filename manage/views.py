# coding:utf-8
# views of manage
import re
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth import (authenticate, login, logout)
from django.template import RequestContext
from blog.models import BasicSettings, Tags, ThreadTypes, Posts, Status
from django.db import transaction
# own import
from pycms import settings
from manage.forms import MakePostForm, ModifyPostForm
from blog.data import UserInfo, BasicInfo
from blog.data import APost as APost


blog_login_url = settings.BLOG_LOGIN_URL


# 公用的添加一个图片自动等比例缩放的js的函数，适合于字符串
def new_post(mkp_form, request):
    """make a new post form a makepost form in web page,return a Posts object."""
    newpost = Posts()
    newpost.init()
    newpost.authorid = int(request.user.id)
    newpost.title = mkp_form.cleaned_data['title']
    newpost.name = mkp_form.cleaned_data['short_title']  # 缩略名
    newpost.cover = mkp_form.cleaned_data['cover_url']
    newpost.introduction = mkp_form.cleaned_data['introduction']
    newpost.content = js_resize_img(mkp_form.cleaned_data['content'])
    newpost.status = Status.objects.get(id=2)  # id为2是已发布的文章，默认为已发布，后面再改
    tagids = mkp_form.cleaned_data['tags']
    if len(tagids) != 0:
        for tagid in tagids:
            tagid = int(tagid)
            tag = Tags.objects.get(id=tagid)
            newpost.tags.add(tag)
    threadtypeid = mkp_form.cleaned_data['threadtypeid']
    newpost.threadtypeid = ThreadTypes.objects.get(id=threadtypeid)
    if mkp_form.cleaned_data['commentnotshow'] != '':
        newpost.comment_status = False
    else:
        newpost.comment_status = True
    return newpost


def change_post(mfp_form, request):
    """change a exist post form a modifypost form in web page,return a Posts object."""
    article_id = int(mfp_form.cleaned_data['id'])
    newpost = APost(article_id)
    if newpost.exist:
        newpost.article.title = mfp_form.cleaned_data['title']
        # 缩略名
        newpost.article.short_title = mfp_form.cleaned_data['short_title']
        newpost.article.cover = mfp_form.cleaned_data['cover_url']
        newpost.article.introduction = mfp_form.cleaned_data['introduction']
        newpost.article.content = mfp_form.cleaned_data['content']
        # id为2是已发布的文章，默认为已发布，后面再改
        newpost.article.status = Status.objects.get(id=2)
        tagids = mfp_form.cleaned_data['tags']
        if len(tagids) != 0:
            for tagid in tagids:
                tagid = int(tagid)
                tag = Tags.objects.get(id=tagid)
                newpost.article.tags.add(tag)
        threadtypeid = int(mfp_form.cleaned_data['threadtypeid'])
        newpost.article.threadtypeid = ThreadTypes.objects.get(id=threadtypeid)
        if mfp_form.cleaned_data['commentnotshow'] != '':
            newpost.article.comment_status = False
        else:
            newpost.article.comment_status = True
        return newpost.article
    else:
        return False


def js_resize_img(text):
    """返回一串在<img />标签中被添加了一段自动调整显示大小的js引用的文本对象"""
    bold = re.compile(r'(<img.+?)/>')
    return bold.sub(r'\1 onload="javascript:DrawImage(this,600,600)" />', text)


@login_required(login_url=blog_login_url)
def home_view(request):
    data = request.extra_data
    return render_to_response('manage/base.html', locals())


@login_required(login_url=blog_login_url)
@transaction.commit_on_success
def make_post_view(request):
    """make post page.It generate the make_post page and receive
    data form the page then store them into database."""
    # get方法，显示表单页面
    data = request.extra_data
    if request.method == 'GET':
        mkp_form = MakePostForm()
        return (
            render_to_response(
                'manage/make_post.html',
                locals(),
                context_instance=RequestContext(request))
        )
    # post方法提交表单并跳转
    if request.method == 'POST':
        mkp_form = MakePostForm(request.POST)
        # Posts.objects.get(id='1')
        if mkp_form.is_valid():
            newpost = new_post(mkp_form, request)
            newpost.save()
            return (
                HttpResponseRedirect(
                    data['basic_info'].blog_edit_url + '/' + str(newpost.id) + '/')
            )
        else:
            return (
                render_to_response(
                    'manage/make_post.html',
                    locals(),
                    context_instance=RequestContext(request))
            )
# 修改文章


@login_required(login_url=blog_login_url)
@transaction.commit_on_success
def modify_post_view(request):
    data = request.extra_data
    article_id = data.get('article_id', 0)
    # get方法，显示表单页面
    if request.method == 'GET':
        a_post = APost(article_id)
        mfp_form = ModifyPostForm()
        if a_post.exist:
            return (
                render_to_response(
                    'manage/modify_post.html',
                    locals(),
                    context_instance=RequestContext(request))
            )
        else:
            raise Http404
    # post方法提交表单并跳转
    elif request.method == 'POST':
        mfp_form = ModifyPostForm(request.POST)
        if mfp_form.is_valid():
            newpost = change_post(mfp_form, request)
            if newpost:
                newpost.save()
                return HttpResponseRedirect(request.path)
            else:
                return "Post does not exist"
        else:
            return (
                render_to_response(
                    'manage/modify_post.html',
                    locals(),
                    context_instance=RequestContext(request))
            )
