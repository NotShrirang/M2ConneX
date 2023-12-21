from django.db import models

from CODE.models import CODEBaseModel
from users.models import AlumniPortalUser


class Experience(CODEBaseModel):
    user = models.ForeignKey(
        AlumniPortalUser, on_delete=models.CASCADE, related_name='experiences')
    company = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    description = models.TextField()
    startDate = models.DateField()
    endDate = models.DateField(null=True, blank=True)
    isCurrent = models.BooleanField(default=False)

    class Meta:
        db_table = 'experience'
        verbose_name = 'Experience'
        verbose_name_plural = 'Experiences'

    def __str__(self):
        return f"{self.user} - {self.company} - {self.designation}"
