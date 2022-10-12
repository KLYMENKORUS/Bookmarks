from django.contrib import admin
from .models import Image, Comment


# Register your models here.
@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'image', 'created']
    list_filter = ['created']


@admin.register(Comment)
class CommentImageAdmin(admin.ModelAdmin):
    list_display = ('image', 'author', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('body',)
