#coding:utf-8
import MySQLdb
import sys,os
from datetime import *
#设置系统环境以便在登记昂哦shell外部引用models功能
sys.path.append(os.path.join(os.path.dirname(__file__),'').replace('\\','/'),)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pycms.settings")
from pycms import settings
from django.contrib.auth.models import User
from django.core import management
#系统环境设置完毕
#db create settings
dbname = 'pycms'
root_username = 'root'
root_passwd = '19921226'
new_username = 'pycms'
passwd_to_set = '19921226'
#super user info
su_name = 'winkidney'
su_email = "winkidney@gmail.com"
su_passwd = "19921226"

def create_db_and_user(dbname,root_username,root_passwd,new_username,passwd_to_set):
    try:
        conn=MySQLdb.Connect(host='localhost',user=root_username,passwd=root_passwd)
        cursor =conn.cursor()
        cursor.execute('CREATE DATABASE `%s` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;' % (dbname))
        print " db created"
    except:
        print "db create failed,check your settings of root_username and passwd"
    try:
        cursor.execute("GRANT ALL PRIVILEGES ON `%s`.* TO '%s'@'localhost' IDENTIFIED BY '%s' WITH GRANT OPTION;" % (dbname,new_username,passwd_to_set)) #CREATE USER user01@'localhost' IDENTIFIED BY 'password1';
        cursor.execute('FLUSH PRIVILEGES;')
        print "db user created"
    except:
        print "db user create failed"
def syncdb_with_su(su_name, su_email, su_passwd):
    #sync db
    management.call_command('syncdb', interactive=False)
    print "sync done"
    #create super user
    user = User.objects.create_superuser(su_name, su_email, su_passwd)
    #user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
    user.save()
    print "super user added"
def add_info():
    from blog.models import *
    basic_settings = {'page_title':u"玻璃齿轮",
                      'logo_txt1':u'Glass',
                      'logo_txt2':u'Gear',
                      'domain':u'',
                      'logo_url':u'',
                      'comment_on':True,
                      'signin_on':False,
                      'site_name':'一个新的玻璃齿轮'
                      }
    for key in basic_settings:
        bs = BasicSettings()
        bs.variable = key
        bs.value = basic_settings[key]
        bs.save()
    #create thread info
    for status_name in (u'草稿',u'已发布',u'已删除'):
        apple = Status()
        apple.status_name = status_name
        apple.save()


    threadtype = ThreadTypes()
    threadtype.display_order = 0 #display order为0首页不显示
    threadtype.name = u'未分类'
    threadtype.parent_id = 0
    threadtype.save()
    
    print "info added"
def add_private_info(): #放在add_info之前，否则分类顺序无法正常显示
    from blog.models import *
    pthreadtypes = (
                    (u'技术',u'娱乐',u'生活'),
                    (
                     (u'Python Web',u'Linux桌面',u'服务器技术',u'前端设计',u'ACG&图形',u'Mysql&Shell',),
                     (u'文摘',u'杂谈',u'艺术（伪）'),
                     (u'影视',u'音乐&视频存档',u'渣文',)
                    )
                   )
    i = 1
    for name in threadtypes[0]:  #创建一个父分类，id为1234
        threadtype = ThreadTypes()
        threadtype.display_order = i
        threadtype.name = name
        threadtype.parent_id = 0
        threadtype.save()
        i+=1
    i = 1
    j = 1
    for child in threadtypes[1]:
        for threadtype in child:
            threadtype = ThreadTypes()
            threadtype.display_order = i
            threadtype.name = name
            threadtype.parent_id = j
            threadtype.save()
            i+=1
        j+=1
if __name__ == "__main__":
    create_db_and_user(dbname,root_username,root_passwd,new_username,passwd_to_set)
    syncdb_with_su(su_name, su_email, su_passwd)
    add_private_info()
    add_info()



