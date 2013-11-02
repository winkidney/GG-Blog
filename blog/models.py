#coding:utf-8
#blog models
from django.db import models
#from tinymce.models import HTMLField

# Create your models here.
#基础设置
class BasicSettings(models.Model):
    variable = models.CharField(max_length=30,verbose_name=u'变量')
    value = models.CharField(max_length=100,verbose_name=u'变量值')
    def __unicode__(self):
        return u"%s" % (self.variable)
    class Meta:
        ordering = ['variable']
#文章状态
class Status(models.Model):
    status_name = models.CharField(max_length=20,verbose_name=u'状态')
    def __unicode__(self):
        return u"%s %s" % (self.id,self.status_name)
    class Meta:
        ordering = ['id']
#标签
class Tags(models.Model):
    tagname = models.CharField(max_length=20,verbose_name=u'标签名称')
    def __unicode__(self):
        return u"%s %s" % (self.id,self.tagname)
    class Meta:
        ordering = ['id']
#分类    
class ThreadTypes(models.Model):
    """If parent_id is 0 ,it's a parent thread type.If not ,it's a child thread type."""
    display_order = models.IntegerField(verbose_name=u'显示顺序')
    name = models.CharField(max_length=40,verbose_name=u'分类名')
    description = models.CharField(max_length=100,blank=True,verbose_name=u'描述')
    status = models.CharField(max_length=20,blank=True,verbose_name=u'分类状态')
    parent_id = models.IntegerField(verbose_name=u"父分类id")
    def __unicode__(self):
        return u"pid:%s ,id:%s,%s" % (self.parent_id,self.id,self.name)
    class Meta:
        ordering = ['parent_id','id','name']
class Comments(models.Model):
    #整型字段好像不能为空，所以将blank=True去掉。
    post_id = models.BigIntegerField(verbose_name=u'评论对应文章id')
    author = models.CharField(max_length=20,verbose_name=u'评论作者')
    author_email = models.EmailField(verbose_name=u'评论者电子邮件')
    author_url = models.URLField(blank=True,verbose_name=u'评论者主页')
    author_ip = models.IPAddressField(blank=True,verbose_name=u'评论者ip地址')
    date = models.DateTimeField(auto_now_add=True,verbose_name=u'评论日期')
    content = models.TextField(verbose_name=u'评论内容')
    approved = models.BooleanField(blank=True,verbose_name=u'评论打开')
    agent = models.CharField(max_length=30,blank=True,verbose_name=u'评论者浏览器')
    parent_id = models.BigIntegerField(verbose_name=u'父评论id')
    user_id = models.BigIntegerField(verbose_name=u'评论者uid')
    def __unicode__(self):
        return u"%s" % self.date
    class Meta:
        ordering = ['id']
class Links(models.Model):
    name = models.CharField(max_length=20,verbose_name=u'链接名称')
    image_url = models.URLField(blank=True,verbose_name=u'链接图片名')
    target_url = models.URLField(verbose_name=u'链接目标地址')
    description = models.TextField(blank=True,verbose_name=u'链接描述')
    visible = models.BooleanField(verbose_name=u'链接可见')
    owner = models.IntegerField(verbose_name=u'链接所有者id') #链接添加者的用户id
    rating = models.IntegerField(blank=True,verbose_name=u'链接受欢迎度')
    rss = models.URLField(blank=True,verbose_name=u'rss链接')
    def __unicode__(self):
        return u"%s" % self.owner
    class Meta:
        ordering = ['id']    
    
#文章
class Posts(models.Model):
    #多对多，外键字段全部设置为可以为空。
    authorid = models.IntegerField(verbose_name=u'文章作者id')
    publish_date = models.DateTimeField(auto_now_add=True,verbose_name=u'发表日期')
    modified_date = models.DateTimeField(auto_now=True,verbose_name=u'最后修改日期')
    content = models.TextField(verbose_name=u'文章内容')
    title = models.CharField(max_length=50,verbose_name=u'文章标题')
    short_title = models.CharField(max_length=50,blank=True,verbose_name=u'文章别名')     #文章缩略名
    cover = models.CharField(max_length=200,verbose_name=u'文章封面图片地址')      #封面图片地址
    introduction = models.CharField(max_length=500,blank=True,verbose_name=u'文章简介')     #文章介绍，将会出现在首页
    status = models.ForeignKey(Status,blank=True,verbose_name=u'文章状态')
    comment_status = models.BooleanField(blank=True,verbose_name=u'不显示评论')
    password = models.CharField(max_length=20,blank=True,verbose_name=u'文章密码')
    tags = models.ManyToManyField(Tags,blank=True,verbose_name=u'标签')
    threadtypeid = models.ForeignKey(ThreadTypes,blank=True,verbose_name=u'分类')
    comment_count = models.IntegerField(verbose_name=u'评论数量')
    comments = models.ManyToManyField(Comments,blank=True,verbose_name=u'评论')
    def init(self):
        self.threadtypeid_id = 1
        self.authorid = 1
        self.status_id = 1
        self.content = ''
        self.title = ''
        self.cover = ''
        self.comment_count = 0
        self.save()
    def __unicode__(self):
        return u"%s %s %s" % (self.id,self.title,self.publish_date)
    class Meta:
        ordering = ['-publish_date']
        
#class Attachments(models.Modle):
#class TestModel(models.Model):
#    content = HTMLField()

#class Author(models.Model):
#    first_name = models.CharField(max_length=30)
#    last_name = models.CharField(max_length=40)
#    email = models.EmailField(blank=True,verbose_name='e-mail')
#    
#    def __unicode__(self):
#        return u'%s %s'% (self.first_name,self.last_name)
#    class Meta:
#        ordering = ['first_name']
#        
#class Book(models.Model):
#    title = models.CharField(max_length = 100)
#    authors = models.ManyToManyField(Author)
#    publisher = models.ForeignKey(Publisher)
#    publication_date = models.DateField()
#    #num_pages = models.IntegerField(blank=True, null=True)
#    
#    def __unicode__(self):
#        return self.title
#    class Meta:
#        ordering = ['title']
#    