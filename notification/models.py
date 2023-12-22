from django.db import models
from CODE.models import CODEBaseModel
from users.models import AlumniPortalUser


class Notification(CODEBaseModel):

    NOTIFICATION_TYPE_CHOICES = (
        ('EVENT', 'EVENT'),
        ('CONNECTION_REQUEST', 'CONNECTION_REQUEST'),
        ('CONNECTION_ACCEPTED', 'CONNECTION_ACCEPTED'),
        ('OPPORTUNITY', 'OPPORTUNITY'),
        ('LIKE', 'LIKE'),
        ('COMMENT', 'COMMENT'),
    )

    title = models.CharField(max_length=100, null=False)
    link = models.CharField(max_length=300, null=False)
    notificationType = models.CharField(
        max_length=100, choices=NOTIFICATION_TYPE_CHOICES, null=False)
    user = models.ForeignKey(
        AlumniPortalUser, on_delete=models.CASCADE, null=False, related_name='notifications')
    isRead = models.BooleanField(default=False, null=False)

    class Meta:
        db_table = 'notification'
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ['-createdAt']
        managed = True

    def __str__(self):
        return self.title + ' - ' + self.user.email
