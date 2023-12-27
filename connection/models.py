from django.db import models

from CODE.models import CODEBaseModel
from users.models import AlumniPortalUser


class Connection(CODEBaseModel):

    CONNECTION_STATUS_CHOICES = (
        ('pending', 'pending'),
        ('accepted', 'accepted'),
        ('rejected', 'rejected'),
    )

    userA = models.ForeignKey(
        to=AlumniPortalUser, on_delete=models.CASCADE, related_name='userA')
    userB = models.ForeignKey(
        to=AlumniPortalUser, on_delete=models.CASCADE, related_name='userB')
    status = models.CharField(
        max_length=20, choices=CONNECTION_STATUS_CHOICES, default='pending')

    class Meta:
        unique_together = ('userA', 'userB')
        db_table = 'connection'
        verbose_name_plural = "connection"
        managed = True

    def __str__(self) -> str:
        return f"{self.userA} >-- {self.status} --< {self.userB}"
