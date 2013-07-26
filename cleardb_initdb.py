#coding:utf-8
import MySQLdb
import sys,os
from blog.models import *
dbname = 'pycms'
rootusername = 'root'
root_passwd = '19921226'
tables_to_delete = 'blog_comments,blog_links,blog_posts,blog_posts_post_tagid,blog_tags,blog_threadtypes,blog_status,blog_posts_post_comments;'#
#try:
#	sys.argv[1] and sys.argv[2]
#except :
#	print "use create_db.py "
#	sys.exit()
#db_name = str(sys.argv[1])
#passwd = str(sys.argv[2])
try:
	conn=MySQLdb.Connect(host='localhost',user=rootusername,passwd=root_passwd)
	cursor =conn.cursor()
	cursor.execute('use %s' % dbname)
	cursor.execute('drop table %s' % tables_to_delete)  #CREATE USER user01@'localhost' IDENTIFIED BY 'password1';
	#conn.commit() 
except Exception, e:
    print 'modified database failed,errors below may help you'
    print e 
finally:
	print 'clear done,start syncdb'
	os.system('python manage.py syncdb')
	print "syncdb done"
print "start init db"
for status_name in (u'草稿',u'已发布',u'已删除'):
	apple = Status()
	apple.status_name = status_name
	apple.save()
threadtype = ThreadTypes()
threadtype.display_order = 0
threadtype.name = u'未分类'
threadtype.save()
