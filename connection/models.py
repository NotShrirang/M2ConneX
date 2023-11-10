from django.db import models
from uuid import uuid4
from users.models import AdminPortalUser

# Create your models here.
class Connection(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    userA = models.ForeignKey(to= AdminPortalUser, on_delete=models.CASCADE, related_name='userA')
    userB = models.ForeignKey(to= AdminPortalUser, on_delete=models.CASCADE, related_name='userB')
    