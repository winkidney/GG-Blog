#coding:utf-8
#file in folder blog
from django.contrib.syndication.views import Feed
from blog.models import Posts

class LatestPostsFeed(Feed):
    title = "BLOG LASTEST"
    link = "/lastestposts/"
    description = "The latest posts on blog."

    def items(self):
        return Posts.objects.filter(status__id=2).order_by('-publish_date')[:10]
    def item_title(self, item):
        return item.title
    def item_pubdate(self, item):
        return item.publish_date
    def item_description(self, item):
        return item.introduction
    def item_link(self, item):
        return item.get_absolute_url()
