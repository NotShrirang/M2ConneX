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
        'payPerMonth',
        'isPaid',
        'user',
        'type',
        'companyName',
        'startDate',
        'endDate',
        'location',
        'workMode',
    )
    list_filter = (
        'createdAt',
        'updatedAt',
        'isActive',
        'user',
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
