# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Connection


@admin.register(Connection)
class ConnectionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'createdAt',
        'updatedAt',
        'isActive',
        'userA',
        'userB',
        'status',
    )
    list_filter = ('createdAt', 'updatedAt', 'isActive', 'userA', 'userB')
