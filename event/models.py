from django.db import models
from uuid import uuid4
from users.models import AdminPortalUser

# Create your models here.
class Event(models.Model):

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
    name = models.TextField(blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    date = models.DateField(blank=False, null=False)    
    time = models.TimeField(blank=False, null=False)
    venue = models.TextField(blank=False, null=False)
    department = models.TextField(blank=False, null=False,choices=DEPARTMENT_CHOICES)

    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

