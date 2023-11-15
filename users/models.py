from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField
from uuid import uuid4
from rest_framework_simplejwt.tokens import RefreshToken
from csc.models import City
from CODE.models import CODEBaseModel


class AlumniPortalUserManager(BaseUserManager):
    def create_user(self, email, password, identifier=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email")

        user = self.model(
            email=self.normalize_email(email),
            identifier=identifier,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class AlumniPortalUser(AbstractBaseUser, PermissionsMixin):

    PRIVILEGE_CHOICES = (
        ('1', 'Super Admin'),
        ('2', 'Staff'),
        ('3', 'Alumni'),
        ('4', 'Student'),
    )

    DEPARTMENT_CHOICES = (
        ('1', 'Computer Engineering'),
        ('2', 'Mechanical Engineering'),
        ('3', 'Electronics & Telecommunication Engineering'),
        ('4', 'Electrical Engineering'),
        ('5', 'Information Technology'),
        ('6', 'Artificial Intelligence & Data Science'),
        ('7', 'First Year Engineering'),
        ('8', 'MBA')
    )

    SIGN_IN_METHOD = (
        ("google", "google"),
        ("email", "email"),
    )

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    identifier = models.CharField(max_length=255, unique=True, blank=True, null=True)
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    firstName = models.CharField(max_length=255, blank=False, null=False)
    lastName = models.CharField(max_length=255, blank=False, null=False)
    department = models.CharField(max_length=255, blank=True, null=True, choices=DEPARTMENT_CHOICES)
    privilege = models.CharField(max_length=255, blank=True, null=True, choices=PRIVILEGE_CHOICES)
    bio = models.TextField(null=True, blank=True)
    resume = models.URLField(max_length=255, blank=True, null=True)
    profilePicture = models.URLField(max_length=255, blank=True, null=True)
    resume = models.URLField(max_length=255, blank=True, null=True)
    city = models.ForeignKey(to=City, on_delete=models.CASCADE, related_name='users', blank=True, null=True)
    phoneNumber = PhoneNumberField(blank=True, null=True)
    signInMethod = models.CharField(max_length=255, blank=True, null=True, choices=SIGN_IN_METHOD)

    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    isVerified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = AlumniPortalUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstName', 'lastName']

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    class Meta:
        db_table = 'alumni_portal_user'


class Alumni(CODEBaseModel):
    user = models.OneToOneField(to=AlumniPortalUser, on_delete=models.CASCADE, related_name='alumni')
    batch = models.IntegerField(blank=False, null=False)
    enrollmentYear = models.DateTimeField(blank=False, null=False)
    passingOutYear = models.DateTimeField(blank=False, null=False)

    def __str__(self):
        return self.user.email

    class Meta:
        db_table = 'alumni'
        verbose_name = 'Alumni'
        verbose_name_plural = 'Alumni'


class Student(CODEBaseModel):
    user = models.OneToOneField(to=AlumniPortalUser, on_delete=models.CASCADE, related_name='student')
    batch = models.IntegerField(blank=False, null=False)
    enrollmentYear = models.DateTimeField(blank=False, null=False)
    passingOutYear = models.DateTimeField(blank=False, null=False)

    def __str__(self):
        return self.user.email

    class Meta:
        db_table = 'student'
        verbose_name = 'Student'
        verbose_name_plural = 'Students'


class Faculty(CODEBaseModel):
    user = models.OneToOneField(to=AlumniPortalUser, on_delete=models.CASCADE, related_name='staff')
    college = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self):
        return self.user.email

    class Meta:
        db_table = 'faculty'
        verbose_name = 'Faculty'
        verbose_name_plural = 'Faculty'


class SuperAdmin(CODEBaseModel):
    user = models.OneToOneField(to=AlumniPortalUser, on_delete=models.CASCADE, related_name='superAdmin')

    def __str__(self):
        return self.user.email

    class Meta:
        db_table = 'super_admin'
        verbose_name = 'Super Admin'
        verbose_name_plural = 'Super Admins'