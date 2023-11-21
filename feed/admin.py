# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Feed, FeedImage, FeedAction, FeedActionComment


@admin.register(Feed)
class FeedAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'createdAt',
        'updatedAt',
        'isActive',
        'subject',
        'body',
        'user',
        'isPublic',
    )
    list_filter = ('createdAt', 'updatedAt', 'isActive', 'user', 'isPublic')


@admin.register(FeedImage)
class FeedImageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'createdAt',
        'updatedAt',
        'isActive',
        'feed',
        'image',
        'coverImage',
    )
    list_filter = (
        'createdAt',
        'updatedAt',
        'isActive',
        'feed',
        'coverImage',
    )


@admin.register(FeedAction)
class FeedActionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'createdAt',
        'updatedAt',
        'isActive',
        'feed',
        'action',
        'user',
    )
    list_filter = ('createdAt', 'updatedAt', 'isActive', 'feed', 'user')


@admin.register(FeedActionComment)
class FeedActionCommentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'createdAt',
        'updatedAt',
        'isActive',
        'feedAction',
        'comment',
    )
    list_filter = ('createdAt', 'updatedAt', 'isActive', 'feedAction')
