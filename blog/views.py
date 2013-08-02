#coding:utf-8
#views of blog
#from django.shortcuts import redirect
#from django.contrib.auth.decorators import user_passes_test
#from django.contrib.auth.decorators import permission_required
from blog.forms import ReplyForm,ReplyFormLogined
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import (authenticate, login ,logout)
from django.template import RequestContext
from django.contrib.auth.models import User
from blog.models import *
#own import 
from pycms import settings

blog_login_url = settings.BLOG_ROOT_URL+'login/'
login_html = 'blog/login/login_django.html'
#获取站点基本信息
def get_basic_info():
    basic_info = {}
    try :
        for key in BasicSettings.objects.all():
            basic_info[key.variable] = key.value
        return basic_info
    except :
        return None
    
def home(request):
    #login检测包装
    if get_basic_info != None:
        basic_info = get_basic_info()
        return render_to_response('blog/base.html',{'static_root':settings.BLOG_STATIC_URL,'basic_info':basic_info})
    else:
        return HttpResponse("error,check basic_info")
def login_view(request):
    site_name = BasicSettings.objects.get(variable='site_name').value
    remind = {} #提示信息存储字典
    errors = ''
     #若用户已登陆，则跳转到登出页面
    if request.user.is_authenticated():
        remind = {'info':'您必须先退出登陆 ^_^','button_name':'退出登陆','url_to':BLOG_ROOT_URL+'logout/'}
        return render_to_response('blog/login/remind.html',locals())
    #用户未登陆，转入登陆页面
    else:
        if request.method == 'GET':
                #这里不这么写居然无法登陆，记下来作为教训吧= =
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
    if request.user.is_authenticated():
            notlogin = False
    else:
            notlogin = True
     # 获取基本信息
    
    basic_info = get_basic_info()
    static_root = settings.BLOG_STATIC_URL
    blog_root_url = settings.BLOG_ROOT_URL
    
    if request.method == 'GET':
        comment_form = ReplyForm()
            # 检查文章id是否存在
        try :
            post = Posts.objects.get(id=int(article_id))
        except:
            return HttpResponse(u'文章不存在')
        # 检查文章状态是否为已发布
        if post.post_status.id == 2:
            author_name = User.objects.get(id=post.post_authorid)
            threadtype = post.post_threadtypeid
            tags = post.post_tagid.all()
            return render_to_response('blog/read.html', locals(),context_instance=RequestContext(request))
        else:
            return HttpResponse(u'文章已被删除')
    elif request.method == 'POST':
        #决定验证用表单对象
        if notlogin:
            comment_form = ReplyFrom(request.POST)
        else:
            comment_form = ReplyFormLogined(request.POST)
            
         #根据提交的数据是否合法重新渲染页面或者返回错误信息   
        if comment_form.is_valid():
            return  HttpResponseRedirect('')
        else:
            try:
                post = Posts.objects.get(id=int(article_id))
            except:
                return HttpResponse(u'文章不存在')
            if post.post_status.id == 2:
                author_name = User.objects.get(id=post.post_authorid)
                threadtype = post.post_threadtypeid
                tags = post.post_tagid.all()
                return render_to_response('blog/read.html', locals(),context_instance=RequestContext(request))
    
    
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
