# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import AlumniPortalUser, Alumni, Student, Faculty, SuperAdmin


@admin.register(AlumniPortalUser)
class AlumniPortalUserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'email',
        'firstName',
        'lastName',
        'department',
        'profilePicture',
        'bio',
        'identifier',
        'privilege',
        'resume',
        'city',
        'phoneNumber',
        'signInMethod',
        'password',
        'last_login',
        'createdAt',
        'updatedAt',
        'isVerified',
        'is_active',
        'is_admin',
        'is_staff',
        'is_superuser',
    )
    list_filter = (
        'last_login',
        'city',
        'createdAt',
        'updatedAt',
        'isVerified',
        'is_active',
        'is_admin',
        'is_staff',
        'is_superuser',
    )
    raw_id_fields = ('groups', 'user_permissions')


@admin.register(Alumni)
class AlumniAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'batch',
        'enrollmentYear',
        'passingOutYear',
        'createdAt',
        'updatedAt',
        'isActive',
    )
    list_filter = (
        'user',
        'enrollmentYear',
        'passingOutYear',
        'createdAt',
        'updatedAt',
        'isActive',
    )


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'batch',
        'enrollmentYear',
        'passingOutYear',
        'createdAt',
        'updatedAt',
        'isActive',
    )
    list_filter = (
        'user',
        'enrollmentYear',
        'passingOutYear',
        'createdAt',
        'updatedAt',
        'isActive',
    )


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'college',
        'createdAt',
        'updatedAt',
        'isActive',
    )
    list_filter = ('createdAt', 'updatedAt', 'isActive', 'user')


@admin.register(SuperAdmin)
class SuperAdminAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'createdAt', 'updatedAt', 'isActive')
    list_filter = ('user', 'createdAt', 'updatedAt', 'isActive')
