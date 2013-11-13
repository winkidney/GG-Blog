#coding:utf-8
#the middleware to process the blog data
#by winkidney 2013 11 11
from blog.data import (UserInfo,BasicInfo,APost,HeaderMenu,PostSummary,TagsGetter,
                       ArchivesIndex,get_time_summarys,PostsGetter,CommentsGetter)

class data_md(object):
    """pass some kwargs to view to share public data"""
    def process_view(self, request, view_func, view_args, view_kwargs):
        if 'admin' not in request.path:
            view_kwargs['posts_getter'] =  PostsGetter()
            view_kwargs['user_info'] = UserInfo(request)
            view_kwargs['basic_info'] = BasicInfo(request)
            view_kwargs['header_menu'] = HeaderMenu()
            view_kwargs['comments_getter'] = CommentsGetter()
            view_kwargs['tags_getter'] = TagsGetter()
            return view_func(request, view_args, view_kwargs)
        else:
            return None