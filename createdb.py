#!usr/bin/python
# coding:utf-8
import MySQLdb
import sys
import os
from datetime import *

# 设置系统环境以便在登记昂哦shell外部引用models功能
sys.path.append(os.path.join(os.path.dirname(__file__), '')
                .replace('\\', '/'),)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pycms.settings")
from pycms import settings
from blog.models import *
from django.contrib.auth.models import User
from django.core import management
import sqlite3
# 系统环境设置完毕
try:
    from pycms.localsettings import *
except:
    # db create settings
    dbname = ''
    root_username = ''
    root_passwd = ''
    new_username = ''
    passwd_to_set = ''
    # super user info
    su_name = ''
    su_email = ""
    su_passwd = ""

def create_sqlite_db(dbname):
    try:
        cx = sqlite3.connect("pycms/"+dbname)
        cx.close()
        print "sqlite3_db created"
    except Exception as e:
        print e
    
def create_db_and_user(dbname, root_username, root_passwd,
                       new_username, passwd_to_set):
    try:
        conn = MySQLdb.Connect(
            host='localhost',
            user=root_username,
            passwd=root_passwd)
        cursor = conn.cursor()
        cursor.execute(
            'CREATE DATABASE `%s` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;' %
            (dbname))
        print " db created"
    except:
        print "db create failed,check your settings of root_username and passwd"
    try:
        cursor.execute(
            "GRANT ALL PRIVILEGES ON `%s`.* TO '%s'@'localhost' IDENTIFIED BY '%s' WITH GRANT OPTION;" %
            (dbname, new_username, passwd_to_set))  # CREATE USER user01@'localhost' IDENTIFIED BY 'password1';
        cursor.execute('FLUSH PRIVILEGES;')
        print "db user created"
    except:
        print "db user create failed"


def syncdb_with_su(su_name, su_email, su_passwd):
    # sync db
    management.call_command('syncdb', interactive=False)
    print "sync done"
    # create super user
    user = User.objects.create_superuser(su_name, su_email, su_passwd)
    #user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
    user.save()
    print "super user added"


def add_info():

    basic_settings = {'page_title': u"玻璃齿轮",
                      'logo_txt1': u'Glass',
                      'logo_txt2': u'Gear',
                      'domain': u'',
                      'logo_url': u'',
                      'comment_on': True,
                      'signin_on': False,
                      'site_name': u'一个新的玻璃齿轮',
                      'about_article_id': '2',
                      'short_about':
                      u'这里是一个简短的关于字段，您可以自行修改',
                      }
    for key in basic_settings:
        bs = BasicSettings()
        bs.variable = key
        bs.value = basic_settings[key]
        bs.save()
    # create thread info
    for status_name in (u'草稿', u'已发布', u'已删除'):
        apple = Status()
        apple.status_name = status_name
        apple.save()

    threadtype = ThreadTypes()
    threadtype.display_order = 0  # display order为0首页不显示
    threadtype.name = u'未分类'
    threadtype.parent_id = 2
    threadtype.save()

    print "info added"


def add_private_info():  # 放在add_info之前，否则分类顺序无法正常显示

    threadtypes = (
        (u'技术', u'娱乐', u'生活'),
        (
            (u'Python Web', u'Linux桌面', u'服务器技术',
             u'前端设计', u'ACG&图形', u'Mysql&Shell',),
            (u'文摘', u'杂谈', u'艺术（伪）'),
            (u'影视', u'音乐&视频存档', u'渣文',)
        )
    )
    i = 1
    for name in threadtypes[0]:  # 创建一个父分类，id为1234
        threadtype = ThreadTypes()
        threadtype.display_order = i
        threadtype.name = name
        threadtype.parent_id = 0
        threadtype.save()
        i += 1

    j = 1
    for child in threadtypes[1]:
        i = 1
        for name in child:
            threadtype = ThreadTypes()
            threadtype.display_order = i
            threadtype.name = name
            threadtype.parent_id = j
            threadtype.save()
            i += 1
        j += 1
    # add tags
    tags = [u'杂谈', u'文摘']
    for tag in tags:
        newtag = Tags(tagname=tag)
        newtag.save()


def new_post(title=None, postcontent=None, statusid=None,
             addtag=False, year=None, month=None, day=None):
    """make a new post form a makepost form in web page,return a Posts object."""
    from testdata import test_content
    import datetime
    newpost = Posts()
    newpost.init()
    if year and month and day:
        newpost.publish_date = datetime.date(year, month, day)
    newpost.authorid = 1

    if title:
        newpost.title = title
    else:
        newpost.title = u'果粉那啥不是这些年的事'
    newpost.name = u''  # 缩略名
    newpost.cover = u''
    newpost.introduction = u''
    if postcontent:
        newpost.content = postcontent
    else:
        newpost.content = test_content
    if statusid:
        # id为2是已发布的文章，默认为已发布，后面再改
        newpost.status = Status.objects.get(id=statusid)
    else:
        newpost.status = Status.objects.get(id=2)
    if addtag:
        tagids = [1, 2]
        if len(tagids) != 0:
            for tagid in tagids:
                tagid = int(tagid)
                tag = Tags.objects.get(id=tagid)
                newpost.tags.add(tag)
    newpost.threadtypeid = ThreadTypes.objects.get(id=16)  # 未分类
    newpost.comment_status = False
    newpost.save()


def add_link(link, linkname):
    pass


def add_posts_bydate():
    for year in xrange(2009, 2013):
        for month in xrange(1, 11):
            for day in xrange(1, 3):
                new_post(year, month, day)


def add_posts_bynumber(num):
    i = 0
    while True:
        new_post()
        i += 1
        if i >= num:
            break
    print 'post added'


def add_init_post():
    new_post(
        '一个新的玻璃齿轮',
        '世界上又多了一个玻璃齿轮（好吧完全是模仿workpress233，简直给跪。你可以删除这个该死的first blood。）',
        2)
    new_post(
        '关于',
        '这是一个关于页面，也是第二篇文章，您可以在基础设置里指定关于页面的id，注意，关于页面的状态必须是草稿，这样才能仅在关于页面看到这篇文章。',
        '1')


def install(mysql_db=False):
    if mysql_db:
        create_db_and_user(
                           dbname,
                           root_username,
                           root_passwd,
                           new_username,
                           passwd_to_set)
    else:
        create_sqlite_db(dbname)
    syncdb_with_su(su_name, su_email, su_passwd)
    add_private_info()
    add_info()
    add_init_post()
    # add_posts_bydate()
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "useage: %s [install|add_posts_bydate|add_posts_by_num]" % (sys.argv[0])
    else:
        if sys.argv[1] not in ('install', 'add_posts_bydate', 'add_posts_by_num'):
            print "parament error,useage: %s [install|install_mysql|add_posts_bydate|add_posts_by_num]" % (sys.argv[0])
        if sys.argv[1] == 'install':
            install()
        if sys.argv[1] == 'install_mysql':
            install(True)
        elif sys.argv[1] == 'add_posts_bydate':
            add_posts_bydate()
        elif sys.argv[1] == 'add_posts_bynum':
            add_posts_bynumber(200)
