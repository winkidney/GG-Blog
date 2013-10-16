#coding:utf-8
#views of blog
#from django.shortcuts import redirect
#from django.contrib.auth.decorators import user_passes_test
#from django.contrib.auth.decorators import permission_required
from blog.forms import ReplyForm,ReplyFormLogined
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse,Http404
from django.contrib.auth import (authenticate, login ,logout)
from django.template import RequestContext
from django.contrib.auth.models import User
from blog.models import *
#own import 
from pycms import settings
from blog.data import UserInfo,BasicInfo,APost

blog_login_url = settings.BLOG_ROOT_URL+'login/'
login_html = 'blog/login/login_django.html'

def logined(request):
    if request.user.is_authenticated():
            return False
    else:
            return True    
def home(request):
    user_info = UserInfo(request)
    basic_info = BasicInfo(request)
    return render_to_response('blog/base.html',
                                    locals(),
                                    context_instance=RequestContext(request))
    #return HttpResponse("error,check basic_info")

    
def login_view(request):
    site_name = BasicSettings.objects.get(variable='site_name').value
    remind = {} #提示信息存储字典
    errors = ''
     #若用户已登陆，则跳转到登出页面
    if request.user.is_authenticated():
        remind = {'info':'您必须先退出登陆 ^_^',
                  'button_name':'退出登陆',
                  'url_to':settings.BLOG_ROOT_URL+'logout/'}
        return render_to_response('blog/login/remind.html',locals())
    #用户未登陆，转入登陆页面
    else:
        if request.method == 'GET':
                #这里不这么写居然无法登陆，记下来作为教训吧= =(后来查明原因，是因为不使用RequestContext的话，csrf标签不会被正确处理
            return render_to_response(login_html,{'site_name':site_name},context_instance=RequestContext(request)) 
        #用同一个url处理用户的登陆表单
        elif request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    remind = {'info':'登陆成功，正在为您跳转到主页','url_to':'../'}
                    return render_to_response('blog/login/auto_jump.html',locals())
                    #return HttpResponseRedirect("/account/loggedin/")
                    # Redirect to a success page.
                else:
                    # Return a 'disabled account' error message
                    errors = 'user is inactive '    
            else:
                # Return an 'invalid login' error message.
                errors = "Your username and password didn't match. Please try again."
            return render_to_response(login_html,{'errors':errors,'site_name':site_name},context_instance=RequestContext(request)) 
@login_required(login_url=blog_login_url)
def logout_view(request):
    site_name = u'玻璃齿轮工作室'
    logout(request)
    # Redirect to a success page.
    remind = {'info':u'注销成功，正在为您跳转到主页','url_to':'../'}
    return render_to_response('blog/login/auto_jump.html',locals())



#阅读文章的函数
def articles(request,article_id):
    user_info = UserInfo(request)
    basic_info = BasicInfo(request)
    a_post = APost(int(article_id))
    if request.method == 'GET':
        if not a_post.exist:
            raise Http404
        # 检查文章状态是否为已发布
        if a_post.post['status'].id == 2:
            return render_to_response('blog/read.html', locals(),context_instance=RequestContext(request))
        else:
            return HttpResponse(u'文章已被删除')
    elif request.method == 'POST':
        #决定验证用表单对象
        if user_info.logined:
            return HttpResponse(u'你是作者，评论个毛！')
        else:
            comment_form = ReplyForm(request.POST)
         #根据提交的数据是否合法重新渲染页面或者返回错误信息   
        if not comment_form.is_valid():
            return  render_to_response('blog/read.html', locals(),context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect(request.path)
    
#登陆要求的包装函数
#@login_required(login_url='/accounts/login/')
#def my_view(request):
#    ...
#自定义登陆检测
#def my_view(request):
#    if not request.user.is_authenticated():
#        return redirect('/login/?next=%s' % request.path)

#指定要求检测，根据email check返回值的真假决定是否运行下面的函数。
#def email_check(user):
#    return '@example.com' in user.email
#
#@user_passes_test(email_check, login_url='/login/')
#def my_view(request):
#    ...

#指定权限验证
#@permission_required('polls.can_vote', login_url='/loginpage/')
#def my_view(request):
#    ...
def contact(request):
    return render_to_response('blog/contact.html')
def about(request):
    return render_to_response('blog/about.html')
def auth(request):
    return HttpResponse("developing!")
def test(request):
    return render_to_response("blog/read.html")
