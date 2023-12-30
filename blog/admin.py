# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Blog, BlogComment, BlogAction


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'content',
        'author',
        'keywords',
        'image',
        'isPublic',
        'isDrafted',
        'createdAt',
        'updatedAt',
        'isActive',
    )
    list_filter = (
        'author',
        'isPublic',
        'isDrafted',
        'createdAt',
        'updatedAt',
        'isActive',
    )


@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'comment',
        'user',
        'action',
        'createdAt',
        'updatedAt',
        'isActive',
    )
    list_filter = ('createdAt', 'updatedAt', 'isActive', 'user', 'action')


@admin.register(BlogAction)
class BlogActionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'action',
        'user',
        'blog',
        'createdAt',
        'updatedAt',
        'isActive',
    )
    list_filter = ('createdAt', 'updatedAt', 'isActive', 'user', 'blog')
