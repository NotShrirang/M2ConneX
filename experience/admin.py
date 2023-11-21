# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Experience


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'createdAt',
        'updatedAt',
        'isActive',
        'user',
        'company',
        'designation',
        'description',
        'startDate',
        'endDate',
        'isCurrent',
    )
    list_filter = (
        'createdAt',
        'updatedAt',
        'isActive',
        'user',
        'startDate',
        'endDate',
        'isCurrent',
    )
