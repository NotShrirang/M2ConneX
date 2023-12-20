from django.db import models
from CODE.models import CODEBaseModel
from users.models import AlumniPortalUser


class UserAnalytics(CODEBaseModel):
    ANALYTICS_TYPE = (
        ('profile visit', 'profile visit'),
        ('profile search', 'profile search'),
        ('feed like', 'feed like'),
        ('feed comment', 'feed comment'),
        ('feed share', 'feed share'),
        ('connection', 'connection'),
    )

    profileUser = models.ForeignKey(
        AlumniPortalUser, on_delete=models.CASCADE, related_name='profileUser')
    visitor = models.ForeignKey(
        AlumniPortalUser, on_delete=models.CASCADE, related_name='visitor')
    analyticsType = models.CharField(
        max_length=50, choices=ANALYTICS_TYPE, default='profile visit')

    class Meta:
        db_table = 'user_analytics'
        verbose_name = "User Analytics"
        verbose_name_plural = "User Analytics"
        ordering = ['-createdAt']
        managed = True

    def __str__(self) -> str:
        return f"{self.profileUser.firstName} {self.profileUser.lastName} - {self.visitor.firstName} {self.visitor.lastName}"
