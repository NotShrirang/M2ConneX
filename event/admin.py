# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Event, EventImage


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'createdAt',
        'updatedAt',
        'isActive',
        'name',
        'description',
        'date',
        'time',
        'venue',
        'department',
        'link',
        'createdByUser',
        'isClubEvent',
        'club',
    )
    list_filter = (
        'createdAt',
        'updatedAt',
        'isActive',
        'date',
        'createdByUser',
        'isClubEvent',
        'club',
    )
    search_fields = ('name',)


@admin.register(EventImage)
class EventImageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'createdAt',
        'updatedAt',
        'isActive',
        'event',
        'image',
    )
    list_filter = ('createdAt', 'updatedAt', 'isActive', 'event')
