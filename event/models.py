from django.db import models

from CODE.models import CODEBaseModel


class Event(CODEBaseModel):

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

    name = models.TextField(blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    date = models.DateField(blank=False, null=False)    
    time = models.TimeField(blank=False, null=False)
    venue = models.TextField(blank=False, null=False)
    department = models.TextField(blank=False, null=False, choices=DEPARTMENT_CHOICES)
    link = models.URLField(blank=True, null=True)

    class Meta:
        db_table = 'event'
        verbose_name_plural = "event"
        managed = True

    def __str__(self) -> str:
        return f"{self.name} - {self.department}"
