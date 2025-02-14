from django.contrib import admin
from .models import *


class wblogAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'slug')
    readonly_fields = ('created_at',)


admin.site.register(Blog, wblogAdmin)
# Register your models here.
