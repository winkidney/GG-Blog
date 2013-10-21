#coding:utf8
#classes used in views
from blog.models import BasicSettings,Posts,ThreadTypes
from pycms import settings
from django.contrib.auth.models import User
from blog.forms import ReplyForm

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
    def __init__(self,request):
        self.blog_settings = {}
        try :
            for key in BasicSettings.objects.all():
                self.blog_settings[key.variable] = key.value
        except :
            print ('read '+str(BasicSettings)+'error')
        self.login_url = settings.BLOG_ROOT_URL+'login/'
        self.static_root = settings.BLOG_STATIC_URL
        self.blog_root_url = settings.BLOG_ROOT_URL
        self.path = request.path
class APost(object):
    """Get article info(include its content)"""
    def __init__(self,article_id):
        if self.exist(article_id):
            self.exist = True
            self.init_data()
        else:
            self.exist = False
    def exist(self,article_id):
        try:
            self.article = Posts.objects.get(id=int(article_id))
            return True
        except:
            return False
    def init_data(self):
        self.post = {}
        self.post['id'] = self.article.id
        self.post['author_id'] = self.article.authorid
        self.post['authorname'] = User.objects.get(id=self.article.authorid)
        self.post['post_date_mixed'] = {'year':(str(self.article.publish_date.year)),
                                                'day':str(self.article.publish_date.day),
                                                'month':str(self.article.publish_date.strftime("%b"))}
        self.post['post_date'] = self.article.publish_date
        self.post['modified_date'] = self.article.modified_date
        self.post['content'] = self.article.content
        self.post['title'] = self.article.title
        self.post['short_title'] = self.article.short_title
        self.post['cover'] = self.article.cover
        self.post['introduction'] = self.article.introduction
        self.post['status'] = self.article.status
        self.post['comment_status'] = self.article.comment_status
        self.post['password'] = self.article.password
        self.post['tags'] = self.article.tags.all()
        self.post['threadtypeid'] = self.article.threadtypeid
        self.post['comment_count'] = self.article.comment_count
        self.post['comments'] = self.article.comments.all()
#menu class in headers
class HeaderMenu(object):
    """header info in every page"""
    def __init__(self):
        self.ttypes_display = []
        pthread_types = ThreadTypes.objects.filter(parent_id=0).order_by("display_order")
        for pthread_type in pthread_types:
            if pthread_type.name != u'未分类':
                link = settings.BLOG_ROOT_URL+'threadtypes/'+pthread_type.name+'/'
                thread_type = {'parent':pthread_type,'link':link,'children':[]}
                cthread_types = ThreadTypes.objects.filter(parent_id=pthread_type.id).order_by("display_order")
                for cthread_type in cthread_types:
                    clink = link+cthread_type.name+'/'
                    cttype = {'name':cthread_type.name,'link':clink}
                    thread_type['children'].append(cttype)
                self.ttypes_display.append(thread_type)

class CommentForm(object):
    def __init__(self,request):
        pass
               
        