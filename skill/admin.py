# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Skill, UserSkill


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('id', 'createdAt', 'updatedAt', 'isActive', 'name')
    list_filter = ('createdAt', 'updatedAt', 'isActive')
    search_fields = ('name',)


@admin.register(UserSkill)
class UserSkillAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'createdAt',
        'updatedAt',
        'isActive',
        'user',
        'skill',
        'experience',
    )
    list_filter = ('createdAt', 'updatedAt', 'isActive', 'user', 'skill')
