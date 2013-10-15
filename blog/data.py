#coding:utf8
#classes used in views
from blog.models import BasicSettings
from pycms import settings

class UserInfo(object):
    """
    Usage: userinfo(HttpRequest)
    Get user_info form request object.
    Generate an object to get and store info of web client user.
    Visit userInfo.name userInfo.logined.
    """
    def __init__(self,request):
        if not request:
            return False
        if request.user.is_authenticated():
            self.logined = True
            self.name = request.user.username
        else:
            self.logined = False
            
class BasicInfo(object):
    """include basic_settings in database and some other basic settings"""
    def __init__(self):
        self.blog_settings = {}
        try :
            for key in BasicSettings.objects.all():
                self.blog_settings[key.variable] = key.value
        except :
            raise False
        self.login_url = settings.BLOG_ROOT_URL+'login/'
        self.static_root = settings.BLOG_STATIC_URL
    
class Article(object):
    pass
    
    
        
        