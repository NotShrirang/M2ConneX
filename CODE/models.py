from django.db import models
from uuid import uuid4


class CODEBaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return str(self.id)
