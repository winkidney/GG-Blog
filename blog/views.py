#coding:utf-8
#blog views
#from django.shortcuts import redirect
#from django.contrib.auth.decorators import user_passes_test
#from django.contrib.auth.decorators import permission_required
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import (authenticate, login ,logout)
from django.template import RequestContext
from blog.models import BasicSettings

blog_login_url = '/blog/login/'
def home(request):
    
    #login检测包装
    basic_info = {}
    try :
        for key in BasicSettings.objects.all():
            basic_info[key.variable] = key.value
    except :
        return HttpResponse("error,check it")
    return render_to_response('blog/index.html',{'basic_info':basic_info})
    from django.contrib.auth import authenticate, login
def login_view(request):
    site_name = BasicSettings.objects.get(variable='site_name').value
    errors = ''
     #若用户已登陆，则跳转到登出页面
    if request.user.is_authenticated():
        return render_to_response('blog/login/logout_first.html',locals())
    else:
        if request.method == 'GET':
                #这里不这么写居然无法登陆，记下来作为教训吧= =
            return render_to_response(login_html,{'site_name':site_name},context_instance=RequestContext(request)) 
        elif request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("login successful!")
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
    logout(request)
    # Redirect to a success page.
    return HttpResponse("successful logout!")

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
    return render_to_response("blog/login/login.html")