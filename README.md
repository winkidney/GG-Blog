## 说明：
### Version:0.1
### Lisense:GPLv3 [quick-guide-gplv3](www.gnu.org/licenses/quick-guide-gplv3.html)
###Summary: 
这是一个为了满足wp不能显示文章封面的问题自己做的简单博客系统，目的是发布带有封面和简介的文章。（虽然后来发现直视自己不太了解wp插件的使用方法而已，但还是坚持写完了这个程序）  
### Feature：
1. 一个博客，单用户  
2. 可以提取每篇文章第一张图作为封面（当然，需要你在模板里面自定义。）
3. 集成ueditor和多说评论功能，包含jiathis分享插件。
4. 内置了替换模板功能，修改settings.py 内的CUR_TEMPLATE_NAME即可，模板存放在pycms/templates/default/下，default即未模板名称，模板目录名和模板名称必须一致。
5. 没了，该有的基本都有了，需要的以后按照需求添加吧  

###Requirements:
+ python 2.6+  
+ django 1.5+  
+ python pyquery  
+ duoshuo requirements   [安装多说](https://github.com/duoshuo/duoshuo-python-sdk)


###Install:
如果是简单的使用，配置数据库就可以正常使用 
如果您是mysql数据库，请先打开项目目录中的createdb.py配置数据库创建和博客超级用户信息。  
然后使用
```bash
cd app_dir/pycms/
sh createdb.py

```
程序会自动创建所需数据库和初始数据。


如果您修改了createdb.py文件的配置，也请同时修改settings.py文件的数据库配置。  

然后以你想要的方式部署服务器，静态文件目录在appdir/pycms/static/  
访问主页：http://path_to_your_server/blog/  
访问管理:http://path_to_your_server/blog/admin/  
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

2013.11.18
