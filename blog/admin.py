from django.contrib import admin
from blog.models import *
class StatusAdmin(admin.ModelAdmin):
    list_display = ('id','status_name',)
    search_fields = ('status_name',)
    list_filter = ('status_name',)
    fields = ('status_name',)

class PostsAdmin(admin.ModelAdmin):
    list_display = ('id','title','status','publish_date')
    search_fields = ('title',)
    list_filter = ('status','threadtypeid','tags','publish_date',)   
admin.site.register(BasicSettings)
admin.site.register(Tags)
admin.site.register(ThreadTypes)
admin.site.register(Posts,PostsAdmin)
admin.site.register(Comments)
admin.site.register(Status,StatusAdmin)
admin.site.register(Links)