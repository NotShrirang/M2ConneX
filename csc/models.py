from django.db import models
from CODE.models import CODEBaseModel

class Country(CODEBaseModel):
    name = models.CharField(max_length=255, blank=False, null=False)

    class Meta:
        db_table = 'country'

    def __str__(self) -> str:
        return self.name

class State(CODEBaseModel):
    name = models.CharField(max_length=255, blank=False, null=False)
    country = models.ForeignKey(to=Country, on_delete=models.CASCADE, related_name='states')

    class Meta:
        db_table = 'state'

    def __str__(self) -> str:
        return self.name

class City(CODEBaseModel):
    name = models.CharField(max_length=255, blank=False, null=False)
    state = models.ForeignKey(to=State, on_delete=models.CASCADE, related_name='cities')

    class Meta:
        db_table = 'city'

    def __str__(self) -> str:
        return self.name