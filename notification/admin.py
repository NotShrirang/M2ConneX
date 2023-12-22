# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'link',
        'notificationType',
        'user',
        'isRead',
        'createdAt',
        'updatedAt',
        'isActive',
    )
    list_filter = ('createdAt', 'updatedAt', 'isActive', 'user', 'isRead')
