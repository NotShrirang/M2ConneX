from django.db import models

from CODE.models import CODEBaseModel
from users.models import AlumniPortalUser


class Connection(CODEBaseModel):
    userA = models.ForeignKey(to=AlumniPortalUser, on_delete=models.CASCADE, related_name='userA')
    userB = models.ForeignKey(to=AlumniPortalUser, on_delete=models.CASCADE, related_name='userB')

    class Meta:
        unique_together = ('userA', 'userB')
        db_table = 'connection'
        verbose_name_plural = "connection"
        managed = True

    def __str__(self) -> str:
        return f"{self.userA} <-> {self.userB}"
