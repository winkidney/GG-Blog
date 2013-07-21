from django.contrib import admin
from blog.models import *

admin.site.register(BasicSettings)
admin.site.register(Tags)
admin.site.register(ThreadTypes)
admin.site.register(Posts)
admin.site.register(Status)