from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import AlumniPortalUser

admin.site.site_header = 'MMCOE Alumni Portal Users App Admin'

class AlumniPortalUserAdmin(UserAdmin):
    model = AlumniPortalUser
    list_display = (
        'email',
        'firstName',
        'lastName',
        'department',
        'privilege',
        'is_active',
        'is_admin',
        'is_staff',
        'is_superuser',
    )
    list_filter = (
        'department',
        'privilege',
        'is_active',
        'is_admin',
        'is_staff',
        'is_superuser',
    )
    search_fields = ('email',)
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'firstName', 'lastName', 'password')}),
        ('Department Info', {'fields': ('department',)}),
        ('Privilege Info', {'fields': ('privilege',)}),
        ('Permissions', {'fields': ('is_active', 'is_admin', 'is_staff', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'firstName', 'lastName', 'password1', 'password2', 'department', 'privilege'),
        }),
    )

admin.site.register(AlumniPortalUser, AlumniPortalUserAdmin)