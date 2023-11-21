# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Country, State, City


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'createdAt', 'updatedAt', 'isActive', 'name')
    list_filter = ('createdAt', 'updatedAt', 'isActive')
    search_fields = ('name',)


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'createdAt',
        'updatedAt',
        'isActive',
        'name',
        'country',
    )
    list_filter = ('createdAt', 'updatedAt', 'isActive', 'country')
    search_fields = ('name',)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'createdAt',
        'updatedAt',
        'isActive',
        'name',
        'state',
    )
    list_filter = ('createdAt', 'updatedAt', 'isActive', 'state')
    search_fields = ('name',)
