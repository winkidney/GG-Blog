#coding:utf-8
#the middleware to process the blog data
#by winkidney 2013 11 11
from blog.data import (UserInfo,BasicInfo,APost,HeaderMenu,PostSummary,ArchivesIndex,get_time_summarys,PostsGetter)

class data_md(object):
    """pass some kwargs to view to share public data"""
    def process_view(self, request, view_func, view_args, view_kwargs):
        view_kwargs['posts_getter'] =  PostsGetter()
        view_kwargs['user_info'] = UserInfo(request)
        view_kwargs['basic_info'] = BasicInfo(request)
        view_kwargs['header_menu'] = HeaderMenu()
        return view_func(request, view_args, view_kwargs)