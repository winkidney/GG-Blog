#coding:utf8
#classes used in views
from blog.models import BasicSettings,Posts,ThreadTypes
from pycms import settings
from django.contrib.auth.models import User
from blog.forms import ReplyForm
from django.core.exceptions import ObjectDoesNotExist

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
        self.static_root = settings.BLOG_STATIC_URL+'/'
        self.blog_root_url = settings.BLOG_ROOT_URL+'/'
        self.path = request.path
        self.articles_url = settings.BLOG_ARTICLES_URL+'/'
        if settings.DEBUG:
            self.show_edit = True
class APost(object):
    """Get article info(include its content) from its id."""
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
    def get_next(self):
        try:
            self.next_post = self.article.get_next_by_publish_date()
        except ObjectDoesNotExist:
            self.next_post = None
    def get_pre(self):
        try:
            self.pre_post = self.article.get_previous_by_publish_date()
        except ObjectDoesNotExist:
            self.pre_post = None
    def init_data(self):
        self.get_next()
        self.get_pre()
        self.post = {}
        self.post['id'] = self.article.id
        self.post['author_id'] = self.article.authorid
        self.post['authorname'] = User.objects.get(id=self.article.authorid)
        self.post['pub_date_mixed'] = {'year':(str(self.article.publish_date.year)),
                                                'day':str(self.article.publish_date.day),
                                                'month':str(self.article.publish_date.strftime("%b"))}
        self.post['pub_date'] = self.article.publish_date
        self.post['modified_date'] = self.article.modified_date
        self.post['content'] = self.article.content
        self.post['title'] = self.article.title
        self.post['short_title'] = self.article.short_title
        self.post['cover_url'] = self.article.cover
        self.post['introduction'] = self.article.introduction
        self.post['status'] = self.article.status
        self.post['comment_status'] = self.article.comment_status
        self.post['password'] = self.article.password
        self.post['tags'] = self.article.tags.all() #use all get all many-to-many ojbects,in foreign key relatives.
                                                    #don't need to call all() function,just access it(for example threadtypeid) .
        self.post['tagidlist_u'] = [unicode(e.id) for e in self.post['tags']]
        self.post['threadtypeid'] = self.article.threadtypeid
        self.post['threadtypeid_u'] = unicode(self.article.threadtypeid.id)
        self.post['comment_count'] = self.article.comment_count
        self.post['comments'] = self.article.comments.all()
    
#menu class in headers
class HeaderMenu(object):
    """header info in every page,it display the """
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
class PostSummary(object):
    """Get a post summary by given post,if not exist,return False."""
    def __init__(self,post):
        self.title = post.title
        self.article_id = post.id
        self.authorname = User.objects.get(id=post.authorid)
        self.pub_date = post.publish_date
        self.pub_date_mixed = {'year':(str(post.publish_date.year)),
                                        'day':str(post.publish_date.day),
                                        'month':str(post.publish_date.strftime("%b"))}
        self.tags = post.tags.all()
        self.comment_count = post.comment_count
        self.summary = self.get_post_summary(post.content)
    def get_post_summary(self,html=''):
        """利用html返回一串纯文本"""
        from HTMLParser import HTMLParser
        html = html.strip()
        html = html.strip("\n")
        result = []
        parser = HTMLParser()
        parser.handle_data = result.append
        parser.feed(html)
        parser.close()
        result = "".join(result)
        if len(result) > 300:
            result = result[0:300]
        return result
class ArchivesIndex(object):
    """archives group by publish date"""
    def __init__(self,type="bymonth"):
        if type == "bymonth":
            self.by_month()
    def by_month(self):
        self.bymonth_dict = {}
        months = Posts.objects.dates("publish_date","month")    #return a year_mounth list order by month
        years = Posts.objects.dates("publish_date","year")    #return a year list(datetime object) order by year
        for year in years:
            self.bymonth_dict[str(year.year)] = []
            for date in months:
                if date.year == year.year:
                    self.bymonth_dict[str(year.year)].append(str(date.month))
    def has_nextyear(self,year):
        yearlist = [ykey for ykey in self.bymonth_dict]
        ylen = len(yearlist)
        if year in yearlist and ylen > yearlist.index(year)+1:
            return True
        else:
            return False
    def has_preyear(self,year):
        yearlist = [ykey for ykey in self.bymonth_dict]
        if year in yearlist and yearlist.index(year) > 0:
            return True
        else:
            return False
    def has_nextmonth(self,year,month):
        monthlist = self.bymonth_dict.get(year)
        mlen = len(monthlist)
        if month in monthlist and monthlist.index(month)+1 < mlen:
            return True
        else:
            return False
    def has_premonth(self,year,month):
        monthlist = self.bymonth_dict.get(year)
        mlen = len(yearlist)
        if month in monthlist and mlen > monthlist.index(month):
            return True
        else:
            return False
    def has_next(self,year,month):
        if self.has_nextmonth(year,month):
           return True
        else:
            if self.has_nextyear(year):
                return True
            else:
                return False
    def has_pre(self,year,month):
        if self.has_premonth(year, month):
            return True
        else:
            if self.has_preyear(year):
                return True
            else:
                return False
    def next(self,year,month):
        """get next archive index (year,month) and return it to page and 
        generate a link to next arvhive"""
        months_in_year = self.bymonth_dict.get(year)
        if months_in_year:
            mlen = len(months_in_year)
            mindex = months_in_year.index(month)
            if mlen > 1:
                if mindex+1 < mlen:
                    n_year = year
                    n_month = months_in_year[mindex+1]
            return (n_year,)
        
            
    def by_year(self):
        pass
    def by_day(self):
        pass
        
class CommentForm(object):
    def __init__(self,request):
        pass
               
        