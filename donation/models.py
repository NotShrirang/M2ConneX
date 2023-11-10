from django.db import models

from CODE.models import CODEBaseModel
from users.models import AlumniPortalUser


class Donation(CODEBaseModel):
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
    amount = models.IntegerField(blank=False, null=False)
    user = models.ForeignKey(to=AlumniPortalUser, on_delete=models.CASCADE, related_name='donations')
    department = models.CharField(max_length=255, blank=False, null=False, choices=DEPARTMENT_CHOICES)

    class Meta:
        db_table = 'donation'
        verbose_name_plural = "donation"
        managed = True

    def __str__(self) -> str:
        return f"{self.name} - {self.user}"
