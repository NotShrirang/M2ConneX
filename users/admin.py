from django.contrib import admin

from .models import AlumniPortalUser, Alumni, Student, Faculty, SuperAdmin


@admin.register(AlumniPortalUser)
class AlumniPortalUserAdmin(admin.ModelAdmin):
    list_display = (
        'password',
        'last_login',
        'id',
        'identifier',
        'email',
        'firstName',
        'lastName',
        'department',
        'privilege',
        'bio',
        'profilePicture',
        'resume',
        'city',
        'phoneNumber',
        'signInMethod',
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
        'createdAt',
        'updatedAt',
        'isActive',
        'user',
        'batch',
        'enrollmentYear',
        'passingOutYear',
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
        'createdAt',
        'updatedAt',
        'isActive',
        'user',
        'batch',
        'enrollmentYear',
        'passingOutYear',
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
        'createdAt',
        'updatedAt',
        'isActive',
        'user',
        'college',
    )
    list_filter = ('createdAt', 'updatedAt', 'isActive', 'user')


@admin.register(SuperAdmin)
class SuperAdminAdmin(admin.ModelAdmin):
    list_display = ('id', 'createdAt', 'updatedAt', 'isActive', 'user')
    list_filter = ('createdAt', 'updatedAt', 'isActive', 'user')
