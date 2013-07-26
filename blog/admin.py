from django.contrib import admin
from blog.models import *
class StatusAdmin(admin.ModelAdmin):
    list_display = ('id','status_name',)
    search_fields = ('status_name',)
    list_filter = ('status_name',)
    fields = ('status_name',)
    
admin.site.register(BasicSettings)
admin.site.register(Tags)
admin.site.register(ThreadTypes)
admin.site.register(Posts)
admin.site.register(Comments)
admin.site.register(Status,StatusAdmin)