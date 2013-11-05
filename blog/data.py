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
        self.blog_page_url = self.blog_root_url+'page/'
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
    def get_first_img(self):
        pass
class ArchivesIndex(object):
    """Get a index of archives group by publish date.
    use  __init__(self,year=None, month=None,type="bymonth").
    you can pass year and month than run self.has_next function
    to get a indexed object stand on next exist archive."""
    def __init__(self,year=None, month=None, type="bymonth"):
        self.year,self.month = year,month
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
            return yearlist[yearlist.index(year)+1]
        else:
            return False
    def has_preyear(self,year):
        yearlist = [ykey for ykey in self.bymonth_dict]
        if year in yearlist and yearlist.index(year) > 0:
            return yearlist[yearlist.index(year)-1]
        else:
            return False
    def has_nextmonth(self,year,month):
        monthlist = self.bymonth_dict.get(year)
        mlen = len(monthlist)
        if month in monthlist and monthlist.index(month)+1 < mlen:
            return monthlist[monthlist.index(month)+1]
        else:
            return False
    def has_premonth(self,year,month):
        monthlist = self.bymonth_dict.get(year)
        mlen = len(yearlist)
        if month in monthlist and mlen > monthlist.index(month):
            return monthlist[monthlist.index(month)-1]
        else:
            return False
    def has_next(self):
        """get next archive index {'year':year,'month':month) and return it to page for 
        generating a link to next arvhive"""
        if self.year and self.month:
            year,month = str(self.year),str(self.month)
            next_month = self.has_nextmonth(year,month)
            if next_month:
                self.next = {'year':year,'month':next_month}
                return True
            else:
                next_year = self.has_nextyear(year)
                if next_year:
                    self.next = {'year':next_year,'month':self.bymonth_dict.get(next_year)[0]}
                    return True
                else:
                    return False
    def has_pre(self):
        """get previous archive index {'year':year,'month':month) and return it to page for 
        generating a link to previous arvhive"""
        if self.year and self.month:
            year,month = str(self.year),str(self.month)
            pre_month = self.has_premonth(year, month)
            if pre_month:
                self.pre = {'year':year,'month':pre_month}
                return True
            else:
                pre_year = self.has_preyear(year)
                if pre_year:
                    self.pre = {'year':next_year,'month':self.bymonth_dict.get(next_year)[-1]}
                    return True
                else:
                    return False

    def by_year(self):
        pass
    def by_day(self):
        pass
        
class PageBtnGenerator(object):
    """generate page buttons from the given current page number"""
    def __init__(self,current_page):
        self.cur_btn = int(current_page)
        self.cur_btns = []
        page_nums = []
        count = Posts.objects.count()
        quotient =  count/settings.ARCHIVES_PER_PAGE
        out_ranger = count%settings.ARCHIVES_PER_PAGE
        if out_ranger:
            quotient = quotient+1
        for number in xrange(1,quotient+1):
            page_nums.append(number)
        if quotient < 15:
                self.cur_btns = page_nums 
        elif quotient > 14:
            if self.cur_btn < 7:
                self.cur_btns = page_nums[:14]
            else:
                self.cur_btns = page_nums[self.cur_btn-7:self.cur_btn+6]
        self.has_next(quotient,self.cur_btn)
    def has_next(self,quotient,cur_page):
        if cur_page < quotient:
            self.next = cur_page+1
        else:
            self.next = None
            
class FivePosts(object):                
    def __init__(self):
        pass
    def lasted(self):
        pass
            
                      
        