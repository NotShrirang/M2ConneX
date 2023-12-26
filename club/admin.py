# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Club, ClubMember


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'createdAt',
        'updatedAt',
        'isActive',
        'name',
        'description',
        'logo',
        'website',
        'socialMedia1',
        'socialMedia2',
        'socialMedia3',
        'email',
        'phone',
    )
    list_filter = ('createdAt', 'updatedAt', 'isActive')
    search_fields = ('name',)


@admin.register(ClubMember)
class ClubMemberAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'createdAt',
        'updatedAt',
        'isActive',
        'user',
        'club',
        'position',
        'positionInWords',
        'isClubAdmin',
    )
    list_filter = (
        'createdAt',
        'updatedAt',
        'isActive',
        'user',
        'club',
        'isClubAdmin',
    )
