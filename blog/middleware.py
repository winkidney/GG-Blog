# coding:utf-8
# the middleware to process the blog data
# by winkidney 2013 11 11
from blog.data import (
    UserInfo, BasicInfo, APost, HeaderMenu, PostSummary, TagsGetter,
    ArchivesIndex, PostsGetter, CommentsGetter, TTypeGetter, LinkGetter)


class data_md(object):

    """pass some kwargs to view to share public data"""

    def process_view(self, request, view_func, view_args, view_kwargs):
            request.extra_data = {}
            request.extra_data['basic_info'] = BasicInfo(request)
            if "admin" not in request.path:
                request.extra_data['posts_getter'] = PostsGetter()
                request.extra_data['user_info'] = UserInfo(request)
                request.extra_data['header_menu'] = HeaderMenu()
                request.extra_data['comments_getter'] = CommentsGetter()
                request.extra_data['tags_getter'] = TagsGetter()
                request.extra_data['ttype_getter'] = TTypeGetter()
                request.extra_data['link_getter'] = LinkGetter()
            return None
