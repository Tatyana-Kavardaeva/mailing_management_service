from django.contrib import admin

from blog.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_filter = ('created_at', 'is_published')
    search_fields = ('name', 'descriptions')
    verbose_name = 'Блог'
