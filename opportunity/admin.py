# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Opportunity, OpportunitySkill, OpportunityApplication


@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'createdAt',
        'updatedAt',
        'isActive',
        'name',
        'description',
        'alumni',
        'type',
        'companyName',
        'startDate',
        'endDate',
        'location',
        'locationType',
    )
    list_filter = (
        'createdAt',
        'updatedAt',
        'isActive',
        'alumni',
        'startDate',
        'endDate',
    )
    search_fields = ('name',)


@admin.register(OpportunitySkill)
class OpportunitySkillAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'createdAt',
        'updatedAt',
        'isActive',
        'opportunity',
        'skill',
    )
    list_filter = (
        'createdAt',
        'updatedAt',
        'isActive',
        'opportunity',
        'skill',
    )


@admin.register(OpportunityApplication)
class OpportunityApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'createdAt',
        'updatedAt',
        'isActive',
        'opportunity',
        'applicant',
        'about',
        'status',
    )
    list_filter = (
        'createdAt',
        'updatedAt',
        'isActive',
        'opportunity',
        'applicant',
    )
