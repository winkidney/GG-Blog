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
    display_order = models.IntegerField(verbose_name=u'显示顺序')
    name = models.CharField(max_length=40,verbose_name=u'分类名')
    description = models.CharField(max_length=100,blank=True,verbose_name=u'描述')
    status = models.CharField(max_length=20,blank=True,verbose_name=u'分类状态')
    def __unicode__(self):
        return u"%s %s" % (self.id,self.name)
    class Meta:
        ordering = ['name']
class Comments(models.Model):
    #整型字段好像不能为空，所以将blank=True去掉。
    comment_post_id = models.BigIntegerField(verbose_name=u'评论对应文章id')
    comment_author = models.CharField(max_length=20,verbose_name=u'评论作者')
    comment_author_email = models.EmailField(blank=True,verbose_name=u'评论者电子邮件')
    comment_author_url = models.URLField(blank=True,verbose_name=u'评论者主页')
    comment_author_ip = models.IPAddressField(blank=True,verbose_name=u'评论者ip地址')
    comment_date = models.DateTimeField(verbose_name=u'评论日期')
    comment_content = models.TextField(verbose_name=u'评论内容')
    comment_approved = models.BooleanField(blank=True,verbose_name=u'评论打开')
    comment_agent = models.CharField(max_length=30,blank=True,verbose_name=u'评论者浏览器')
    comment_parent_id = models.BigIntegerField(verbose_name=u'父评论id')
    user_id = models.BigIntegerField(verbose_name=u'评论者uid')
    def __unicode__(self):
        return u"%s" % self.comment_date
    class Meta:
        ordering = ['id']
class Links(models.Model):
    link_name = models.CharField(max_length=20,verbose_name=u'链接名称')
    link_image_url = models.URLField(blank=True,verbose_name=u'链接图片名')
    link_target_url = models.URLField(verbose_name=u'链接目标地址')
    link_description = models.TextField(blank=True,verbose_name=u'链接描述')
    link_visible = models.BooleanField(verbose_name=u'链接可见')
    link_owner = models.IntegerField(verbose_name=u'链接所有者id') #链接添加者的用户id
    link_rating = models.IntegerField(blank=True,verbose_name=u'链接受欢迎度')
    link_rss = models.URLField(blank=True,verbose_name=u'rss链接')
    def __unicode__(self):
        return u"%s" % self.link_owner
    class Meta:
        ordering = ['id']    
    
#文章
class Posts(models.Model):
    #多对多，外键字段全部设置为可以为空。
    post_authorid = models.IntegerField(verbose_name=u'文章作者id')
    post_date = models.DateTimeField(auto_now_add=True,verbose_name=u'发表日期')
    post_date_modified = models.DateTimeField(auto_now=True,verbose_name=u'最后修改日期')
    post_content = models.TextField(verbose_name=u'文章内容')
    post_title = models.CharField(max_length=50,verbose_name=u'文章标题')
    post_name = models.CharField(max_length=50,blank=True,verbose_name=u'文章别名')     #文章缩略名
    post_cover = models.CharField(max_length=200,verbose_name=u'文章封面图片地址')      #封面图片地址
    post_introduction = models.CharField(max_length=500,blank=True,verbose_name=u'文章简介')     #文章介绍，将会出现在首页
    post_status = models.ForeignKey(Status,blank=True,verbose_name=u'文章状态')
    comment_status = models.BooleanField(blank=True,verbose_name=u'不显示评论')
    post_password = models.CharField(max_length=20,blank=True,verbose_name=u'文章密码')
    post_tagid = models.ManyToManyField(Tags,blank=True,verbose_name=u'标签')
    post_threadtypeid = models.ForeignKey(ThreadTypes,blank=True,verbose_name=u'分类')
    post_comment_count = models.IntegerField(verbose_name=u'评论数量')
    post_comments = models.ManyToManyField(Comments,blank=True,verbose_name=u'评论')
    def init(self):
        self.post_threadtypeid_id = 1
        self.post_authorid = 1
        self.post_status_id = 1
        self.post_content = ''
        self.post_title = ''
        self.post_cover = ''
        self.post_comment_count = 0
        self.save()
    def __unicode__(self):
        return u"%s %s %s" % (self.id,self.post_title,self.post_date)
    class Meta:
        ordering = ['post_date']
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