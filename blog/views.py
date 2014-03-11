# coding:utf-8
# views of blog
#from django.shortcuts import redirect
#from django.contrib.auth.decorators import user_passes_test
#from django.contrib.auth.decorators import permission_required
from blog.forms import ReplyForm, ReplyFormLogined
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth import (authenticate, login, logout)
from django.template import RequestContext
import json
from django.contrib.auth.models import User
from blog.models import *
# own import
from pycms import settings
from blog.data import (
    UserInfo, BasicInfo, APost, HeaderMenu, PostSummary, ArchivesIndex, get_summarys_bytime,
    PostsGetter, get_summarys_byttype, get_summarys_bypage, make_comment)
from tools.tools import timeit

blog_login_url = settings.BLOG_LOGIN_URL + '/'
login_html = settings.LOGIN_TEMPLATE
jump_html = settings.JUMP_TEMPLATE
remind_html = settings.REMIND_TEMPLATE

@timeit
def get_page_summarysV2(page_num, num_per_page=10):
    """costs 0.03s whth 10,000 record"""
    from django.core.paginator import Paginator
    page_num = int(page_num)
    num_per_page = int(num_per_page)
    post_summarys = []
    posts = Posts.objects.all()
    pages = Paginator(posts, num_per_page)
    for post in pages.page(page_num):
            post_summarys.append(PostSummary(post))
    return post_summarys


def logined(request):
    if request.user.is_authenticated():
            return True
    else:
            return False
        
        
def get_user(request):
    """get a request and return a user obj"""
    username = request.POST.get('username')
    password = request.POST.get('password')
    return authenticate(username=username, password=password)

    
def home_view(request, *args, **kwargs):
    data = request.extra_data
    page = kwargs.get('pagenum', 1)
    from blog.data import PageBtnGenerator
    pagination = PageBtnGenerator(page)
    if not pagination.exist:
        raise Http404
    if logined(request):
        post_summarys = get_summarys_bypage(page, False)
    else:
        post_summarys = get_summarys_bypage(page, False)
    
    return render_to_response('blog/home.html',
                              locals(),
                              context_instance=RequestContext(request))
    # return HttpResponse("error,check basic_info")


def login_view(request, *args, **kwargs):
    data = request.extra_data
    remind = {}  # 提示信息存储字典
    errors = ''
    # 若用户已登陆，则跳转到登出页面
    if logined(request):
        remind = {'info': '您必须先退出登陆 ^_^',
                  'button_name': '退出登陆',
                  'url_to': settings.BLOG_ROOT_URL + '/logout'}
        html = remind_html
    # 用户未登陆，转入登陆页面
    else:
        if request.method == 'GET':
            html = login_html
        elif request.method == 'POST':
            user = get_user(request)
            html = login_html
            if user:
                if user.is_active:
                    login(request, user)
                    remind = {'info': 'logined!jump to home', 'url_to': data['basic_info'].blog_root_url+'/'}
                    html = jump_html
                else:
                    errors = 'user is inactive '
            else:
                errors = "Your username and password didn't match. Please try again."
    return render_to_response(
                    html,
                    locals(),
                    context_instance=RequestContext(request))

def ajax_login_view(request, *args, **kwargs):
    if request.method == 'POST':
            user = get_user(request)
            res_dict = {'status':'',
                        'username':'',
                        }
            if user is not None:
                if user.is_active:
                    login(request, user)
                    res_dict['status'] = 'success'
                    res_dict['username'] = user.username
                else:
                    res_dict['status'] = 'user not active'
            else:
                res_dict['status'] = 'user not exist'   
            return HttpResponse(json.dumps(res_dict))
    else:
        return HttpResponse('forbidden')


@login_required(login_url=blog_login_url)
def logout_view(request, *args, **kwargs):
    data = request.extra_data
    logout(request)
    # Redirect to a success page.
    remind = {'info': u'注销成功，正在为您跳转到主页', 'url_to': '../'}
    return render_to_response('blog/login/auto_jump.html', locals())


# 阅读文章的函数
def articles_view(request, *args, **kwargs):
    """read articles inclued articles reader and
    comment post function,if articles not found ,it raise a 404 error"""
    data = request.extra_data
    a_post = APost(int(kwargs.get('article_id', 0)))
    if request.method == 'GET':
        if not a_post.exist:
            raise Http404
        # 检查文章状态是否为已发布
        if a_post.post['status'].id == 2:
            return (
                render_to_response(
                    'blog/read.html',
                    locals(),
                    context_instance=RequestContext(request))
            )
        elif a_post.post['status'].id == 1 and logined(request):
            return (
                render_to_response(
                    'blog/read.html',
                    locals(),
                    context_instance=RequestContext(request))
            )
        else:
            raise Http404
    elif request.method == 'POST':
        if user_info.logined:
            return HttpResponse(u'你是作者，评论个毛！')
        else:
            comment_form = ReplyForm(request.POST)
         # 根据提交的数据是否合法重新渲染页面或者返回错误信息
        if not comment_form.is_valid():
            return render_to_response('blog/read.html',
                                      locals(),
                                      context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect(request.path)


def archives_view(request, *args, **kwargs):
    """generate acchives by year_month or archives index by year or year_month"""
    data = request.extra_data
    year, month = kwargs.get('year', None), kwargs.get('month', None)
    data['year'], data['month'] = year, month
    post_summarys = get_summarys_bytime(year, month)
    archives_index = ArchivesIndex(year, month)
    if post_summarys:
        return render_to_response('blog/archives.html',
                                  locals(),
                                  context_instance=RequestContext(request))
    else:
        raise Http404


def archives_index_view(request, *args, **kwargs):
    data = request.extra_data
    archives_index = ArchivesIndex()
    return render_to_response('blog/archives_index.html',
                              locals(),
                              context_instance=RequestContext(request))


def tags_view(request, *arg, **kwargs):
    data = request.extra_data
    tag = kwargs.get('tagname', None)
    data['tagname'] = tag
    tags_getter = data.get('tags_getter', None)
    if tag in tags_getter.tagnamelist:
        from blog.data import get_summarys_bytag
        post_summarys = get_summarys_bytag(tag)
        return render_to_response('blog/read_bytags.html', locals(),context_instance=RequestContext(request))
    else:
        raise Http404


def thread_type_view(request, *arg, **kwargs):
    data = request.extra_data
    ttype = kwargs.get('threadtype', None)
    data['threadtype'] = ttype
    ttype_getter = data.get('ttype_getter', None)
    # 在父分类中，列出子分类目录
    if ttype in ttype_getter.ctypes:
        post_summarys = get_summarys_byttype(ttype)
        html = 'blog/read_byttype.html'
    # 在子分类中，直接显示内容
    elif ttype in ttype_getter.ptypes:
        html = 'blog/ttype_index.html'
    else:
        raise Http404
    return render_to_response(html, locals(),context_instance=RequestContext(request))

# 登陆要求的包装函数
#@login_required(login_url='/accounts/login/')
# def my_view(request):
#    ...
# 自定义登陆检测
# def my_view(request):
#    if not request.user.is_authenticated():
#        return redirect('/login/?next=%s' % request.path)

# 指定要求检测，根据email check返回值的真假决定是否运行下面的函数。
# def email_check(user):
#    return '@example.com' in user.email
#
#@user_passes_test(email_check, login_url='/login/')
# def my_view(request):
#    ...

# 指定权限验证
#@permission_required('polls.can_vote', login_url='/loginpage/')
# def my_view(request):
#    ...


def make_comment_view(request, *args, **kwargs):
    data = request.extra_data
    if request.method == 'GET':
        raise Http404
    elif request.method == 'POST':
        if data.get('user_info').logined:
            return HttpResponse(u'你是作者，评论个毛！')
        comment_form = ReplyForm(request.POST)
        # 根据提交的数据是否合法重新渲染页面或者返回错误信息
        if comment_form.is_valid():
            make_comment(comment_form)
            return HttpResponseRedirect(comment_form.cleaned_data['fnext'])
        else:
            remind = {}  # 提示信息存储字典
            errors = ''
            # 提示信息，提示表单有误
            remind = {'info': '表单填写有误，请您确定填写正确哦 ^_^',
                      'button_name': '返回首页',
                      'url_to': settings.BLOG_ROOT_URL}
            return render_to_response('blog/login/remind.html', locals())
        
        
def ajax_make_comment_view(request, *args, **kwargs):
    data = request.extra_data
    res_dict = {'status':''}
    if request.method == 'GET':
        return HttpResponse('forbidden')
    elif request.method == 'POST':
        comment_form = ReplyForm(request.POST)
        if comment_form.is_valid():
            if not data.get('user_info').logined:
                make_comment(comment_form)
                res_dict['status'] = 'success'
            else:
                res_dict['status'] = u'you are author!'
        else:
            res_dict['status'] = comment_form.errors
        return HttpResponse(json.dumps(res_dict))


def about_view(request, *args, **kwargs):
    """read articles inclued articles reader and
    comment post function,if articles not found ,it raise a 404 error"""
    data = request.extra_data
    article_id = data['basic_info'].blog_settings.get('about_article_id', 0)
    a_post = APost(article_id)
    if request.method == 'GET':
        if not a_post.exist:
            raise Http404
        # 检查文章状态是否为已发布
        html = 'blog/read.html'
        if a_post.post['status'].id == 1:
            pass
        elif a_post.post['status'].id == 2 and logined(request):
            pass
        else:
            raise Http404
        return (
                render_to_response(
                    html,
                    locals(),
                    context_instance=RequestContext(request))
            )

def musicmode_view(request, *args, **kwargs):
    data = request.extra_data
    return (
                render_to_response(
                    "blog/music.html",
                    locals(),
                    context_instance=RequestContext(request))
            )