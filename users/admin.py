# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import AlumniPortalUser, Alumni, Student, Faculty, SuperAdmin, Blogger


@admin.register(AlumniPortalUser)
class AlumniPortalUserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'email',
        'firstName',
        'lastName',
        'department',
        'privilege',
        'phoneNumber',
        'city',
        'identifier',
        'bio',
        'profilePicture',
        'resume',
        'signInMethod',
        'createdAt',
        'updatedAt',
        'last_login',
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
        'isActive',
        'createdAt',
        'updatedAt',
    )
    list_filter = (
        'createdAt',
        'updatedAt',
        'isActive',
        'user',
        'enrollmentYear',
        'passingOutYear',
    )


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'batch',
        'enrollmentYear',
        'passingOutYear',
        'isActive',
        'createdAt',
        'updatedAt',
    )
    list_filter = (
        'createdAt',
        'updatedAt',
        'isActive',
        'user',
        'enrollmentYear',
        'passingOutYear',
    )


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'college',
        'isActive',
        'createdAt',
        'updatedAt',
    )
    list_filter = ('createdAt', 'updatedAt', 'isActive', 'user')


@admin.register(SuperAdmin)
class SuperAdminAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'createdAt', 'updatedAt', 'isActive')
    list_filter = ('createdAt', 'updatedAt', 'isActive', 'user')


@admin.register(Blogger)
class BloggerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'createdAt', 'updatedAt', 'isActive')
    list_filter = ('createdAt', 'updatedAt', 'isActive', 'user')
