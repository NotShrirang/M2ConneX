from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import (
    AlumniPortalUser,
    Alumni,
    Student,
    Faculty,
    SuperAdmin
)

class AlumniPortalUserAdmin(UserAdmin):
    model = AlumniPortalUser
    list_display = (
        'email',
        'firstName',
        'lastName',
        'department',
        'privilege',
        'isVerified',
        'is_active',
        'is_admin',
        'is_staff',
        'is_superuser',
    )
    list_filter = (
        'department',
        'privilege',
        'isVerified',
        'is_active',
        'is_admin',
        'is_staff',
        'is_superuser',
    )
    search_fields = ('email',)
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'firstName', 'lastName', 'password', 'signInMethod')}),
        ('Department Info', {'fields': ('department',)}),
        ('Profile Info', {'fields': ('bio', 'resume', 'profilePicture',)}),
        ('Address Info', {'fields': ('city',)}),
        ('Privilege Info', {'fields': ('privilege',)}),
        ('Permissions', {'fields': ('isVerified', 'is_active', 'is_admin', 'is_staff', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'firstName', 'lastName', 'password1', 'password2', 'department', 'privilege'),
        }),
    )

admin.site.register(AlumniPortalUser, AlumniPortalUserAdmin)
admin.site.register(Alumni)
admin.site.register(Student)
admin.site.register(Faculty)
admin.site.register(SuperAdmin)