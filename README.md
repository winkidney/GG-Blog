## 说明：
### Version:0.1.1
### Lisense:GPLv3 [quick-guide-gplv3](www.gnu.org/licenses/quick-guide-gplv3.html)
###Summary: 
这是一个为了满足wp不能显示文章封面的问题自己做的简单博客系统，目的是发布带有封面和简介的文章。（虽然后来发现只是自己不太了解wp插件的使用方法而已，且觉得wp太臃肿，运行太慢，感觉作为博客有点overweight，所以还是自己写完了这个博客）  

###Feature：
1. 一个博客，单用户  
2. 可以提取每篇文章第一张图作为封面（当然，也可以不要。）
3. 集成ueditor和多说评论功能，包含jiathis分享插件。
4. 内置了替换模板功能，修改settings.py 内的CUR_TEMPLATE_NAME即可，模板存放在pycms/templates/default/下，default即未模板名称，模板目录名和模板名称必须一致。
5. 没了，该有的基本都有了，需要的以后按照需求添加吧  
6. 模板使用了html5标准，需要<blod>现代浏览器</bold>才能正确显示 [DEMO](http://blog.gg-workshop.com)

###ChangeLog
+ 2014-03-11 新建分支release-0.1.1,删除一些未使用的js文件和图片文件，修正一个数据库新建脚本的  错误
+ 06.02.2014 将数据库迁移到sqlite3，并将安装脚本修改为可选择数据库（默认sqlite，可以mysql）；增加support files->example-localsettings-sqlite.py
+ 2013.12.29 增加support files，包含nginx配置文件（fcgi），重启服务和启动服务的脚本，增加localsettings配置文件范例
+ 2013.12.29 修复了一个分页显示错误，增加音乐模式/musicmode/，优化博客后台显示
+ 2013.12.10 添加ajax登录以及评论表单验证，支持不重新登录刷新边栏，修正一些显示错误
+ 2013.11.x 发布0.1并部署成功

###Requirements:
+ python 2.6+  
+ django 1.5+  
+ pyquery  
+ duoshuo requirements   [安装多说](https://github.com/duoshuo/duoshuo-python-sdk)


###Install:
如果需要使用稳定版本，请移步[release-0.1.1](https://github.com/winkidney/GG-Blog/tree/release-0.1.1)
如果是简单的使用，配置数据库就可以正常使用,不过您需要先安装好依赖，例如：

```bash
pip install pyquery
```
期间可能需要安装lxml库，请使用相应的包管理器来安装这些库。    
安装好依赖之后   
如果您选择默认的sqlite数据库
在终端键入
```bash
cd support-file
cp example-localsettings-sqlite.py appdir/pycms/pycms/localsettings.py
```  
将配置文件复制到appdir/pycms/pycms中（settings文件所在目录）
打开配置文件，配置数据库信息,博客超级用户信息，注意上面的数据库配置要跟下面的数据库创建配置一致

```python

# coding:utf-8
# localsettings to protect my info
# in folder pycms
import os
db_root = os.path.join(os.path.dirname(__file__), '').replace('\\', '/')
####
SECRET_KEY = '_c@$un4*ihb4(&hf&556485qi@)yc-x=rw17h05jhe!h#fg^3r'
DEBUG = True
ALLOWED_HOSTS = ['*']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',    # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'
        'NAME': db_root+'pycms.db',
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        # Set to empty string for localhost. Not used with sqlite3.
        'HOST': '',
        # Set to empty string for default. Not used with sqlite3.
        'PORT': '',
    }
}
######多说########
DUOSHUO_SECRET = '578c296aae128ca54179e847cda351f4'
DUOSHUO_SHORT_NAME = 'ggblog'

#########################used by createdb.py##############################
# db create settings
dbname = 'pycms'
#数据库未sqlite时如下数据库数据不需要设置
root_username = ''
root_passwd = '19921226'
new_username = 'pycms'
passwd_to_set = '19921226'
# super user info超级用户信息，需要设置
su_name = 'blog super user'
su_email = "w@gmail.com"
su_passwd = "your password"
##########################ebd of createdb.py used#########################

```

如果您是mysql数据库

第一步复制文件
```bash
cd support-file
cp example-localsettings-sqlite.py appdir/pycms/pycms/localsettings.py
```  
接下来编辑配置文件
```python
SECRET_KEY = ''
DEBUG = True
ALLOWED_HOSTS = ['*']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # your db backend,now the createdb.py only support mysql,not tested on sqlite yet.
        'NAME': 'your db name',
        'USER': 'your db user name',                      # Not used with sqlite3.
        'PASSWORD': 'your db pwd',                  # Not used with sqlite3.
        # Set to empty string for localhost. Not used with sqlite3.
        'HOST': '',
        # Set to empty string for default. Not used with sqlite3.
        'PORT': '3306',
    }
}
######多说########
DUOSHUO_SECRET = 'your duoshuo secret'
DUOSHUO_SHORT_NAME = 'your short name'

#########################used by createdb.py##############################
# db create settings
dbname = 'pycms'
root_username = 'root'
root_passwd = 'your root pwd'
new_username = 'you new db user name'
passwd_to_set = 'your new db user pwd'
# super user info
su_name = 'blog super user name'
su_email = "email"
su_passwd = "blog super user name"
##########################ebd of createdb.py used#########################

```
最后一部，运行安装脚本,在终端中键入    
如果您是sqlite数据库
```bash
cd appdir/pycms/
python createdb.py install
```
如果您是mysql数据库  
```bash  
cd app_dir/pycms/
python createdb.py install_mysql

```  
静静的等待完成吧=w=  
程序会自动创建所需数据库和初始数据。  



接下来，以你想要的方式部署服务器，nginx+fcgi,nginx+uwsgi,apache+mod*。
如果您使用nginx+fcgi（flup），请先安装flup，nginx参考配置文件在support-file文件夹中  
   
静态文件目录在appdir/pycms/static/，建议ln -s 到一个别的目录增加安全性。
访问主页：http://path_to_your_server/  
访问管理:http://path_to_your_server/admin/   
管理页面中您可以按照您的需求修改各种设置。  


结构：  
	基础设置  
	---------about_article_id（int：关于页面的文章id，默认为2，推荐直接编辑id为2的文章，如果自行修改记得将文章状态设置为草稿，不然会显示在主页）
	---------comment_on（int：评论是否打开0 or 1）  
	---------log_txt1（char：log文字1，默认glass）  
	---------log_txt2（char：logo文字2.默认gear）  
	---------logo_url（char：logo图片url，用来替换logo文字或者一起使用。）  
	---------page_title（char：页面标题）  
	---------short_about（char：短自我介绍，会显示在首页页脚）  
	---------seite_name（char：站点名称）  



如果有任何需求或者bug，也请提交给我^_^    
[My E-mail](mailto:winkidney@gmail.com)   
 
[My Blog](http://blog.gg-workshop.com)  

2013.11.18 by winkidney
