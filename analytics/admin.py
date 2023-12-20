# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import UserAnalytics


@admin.register(UserAnalytics)
class UserAnalyticsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'createdAt',
        'updatedAt',
        'isActive',
        'profileUser',
        'visitor',
        'analyticsType',
    )
    list_filter = (
        'createdAt',
        'updatedAt',
        'isActive',
        'profileUser',
        'visitor',
    )
