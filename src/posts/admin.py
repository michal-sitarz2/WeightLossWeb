from django.contrib import admin
from .models import Post


class BlogAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'date')
    search_fields = ('user__username', 'title')

admin.site.register(Post, BlogAdmin)
