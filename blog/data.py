#coding:utf8
#classes used in views
from blog.models import BasicSettings,Posts
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
    
class APost(object):
    """Get article info(include its content)"""
    def __init__(self,article_id):
        if exist(article_id):
            self.exist = True
        else:
            self.exist = False
    def exist(self,article_id):
        try:
            self.article = Posts.objects.get(id=int(article_id))
            return False
        except:
            return True
    def init_data(self):
        self.post[id] = self.article.id
        self.post[author_id] = self.authorid
        self.post[post_date] = self.article.publish_date
        self.post[modified_date] = self.article.modified_date
        self.post[content] = self.article.content
        self.post[title] = self.article.title
        self.post[short_title] = self.article.short_title
        self.post[cover] = self.article.cover
        self.post[introduction] = self.article.introduction
        self.post[status] = self.article.status
        self.post[comment_status] = self.article.comment_status
        
        