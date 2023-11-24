# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Blog, BlogComment, BlogAction


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'createdAt',
        'updatedAt',
        'isActive',
        'title',
        'content',
        'author',
        'isPublic',
        'isDrafted',
    )
    list_filter = (
        'createdAt',
        'updatedAt',
        'isActive',
        'author',
        'isPublic',
        'isDrafted',
    )


@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'createdAt',
        'updatedAt',
        'isActive',
        'comment',
        'user',
        'blog',
    )
    list_filter = ('createdAt', 'updatedAt', 'isActive', 'user', 'blog')


@admin.register(BlogAction)
class BlogActionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'createdAt',
        'updatedAt',
        'isActive',
        'action',
        'user',
        'blog',
    )
    list_filter = ('createdAt', 'updatedAt', 'isActive', 'user', 'blog')
