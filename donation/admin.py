# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Donation


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'createdAt',
        'updatedAt',
        'isActive',
        'name',
        'description',
        'amount',
        'user',
        'department',
    )
    list_filter = ('createdAt', 'updatedAt', 'isActive', 'user')
    search_fields = ('name',)
