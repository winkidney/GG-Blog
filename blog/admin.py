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
    exclude = ('authorid',) 
    def save_model(self, request, modelobj, form, change):
        modelobj.authorid = request.user.id
        modelobj.save()
        modelobj.comment_count = len(modelobj.comments.all())
        modelobj.save()
class LinksAdmin(admin.ModelAdmin):
    list_display = ('id','name','target_url')
class ThreadTypesAdmin(admin.ModelAdmin):
    list_display = ('name','parent_id','id',)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('id','tagname',)
admin.site.register(BasicSettings)
admin.site.register(Tags)
admin.site.register(ThreadTypes,ThreadTypesAdmin)
admin.site.register(Posts,PostsAdmin)
admin.site.register(Comments)
admin.site.register(Status,StatusAdmin)
admin.site.register(Links,LinksAdmin)