# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import OTP


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'otp',
        'isUsed',
        'createdAt',
        'updatedAt',
        'isActive',
    )
    list_filter = ('createdAt', 'updatedAt', 'isActive', 'isUsed')
