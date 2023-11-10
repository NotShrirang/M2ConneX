from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField
from uuid import uuid4
from rest_framework_simplejwt.tokens import RefreshToken
from csc.models import City

class AlumniPortalUserManager(BaseUserManager):
    def create_user(self, email, password, identifier, **extra_fields):
        if not email:
            raise ValueError("Users must have an email")
        if not identifier:
            raise ValueError("Users must have an identifier")
        
        user = self.model(
            email = self.normalize_email(email),
            identifier = identifier,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, identifier, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, identifier, **extra_fields)

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

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    identifer = models.CharField(max_length=255, unique=True, blank=False, null=False)
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    firstName = models.CharField(max_length=255, blank=False, null=False)
    lastName = models.CharField(max_length=255, blank=False, null=False)
    department = models.CharField(max_length=255, blank=False, null=False, choices=DEPARTMENT_CHOICES)
    privilege = models.CharField(max_length=255, blank=False, null=False, choices=PRIVILEGE_CHOICES)
    resume = models.URLField(max_length=255, blank=True, null=True)
    profilePicture = models.URLField(max_length=255, blank=True, null=True)
    city = models.ForeignKey(to=City, on_delete=models.CASCADE, related_name='users', blank=False, null=False)
    phoneNumber = PhoneNumberField(blank=True, null=True)
    
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    objects = AlumniPortalUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['identifer', 'firstName', 'lastName', 'department', 'privilege', 'city']

    def __str__(self):
        return self.email
    
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return{
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        }
    
    class Meta:
        db_table = 'alumni_portal_user'