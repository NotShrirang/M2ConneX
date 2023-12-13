from django.db import models
from CODE.models import CODEBaseModel
from django.utils.translation import gettext_lazy as _


class Country(CODEBaseModel):
    name = models.CharField(verbose_name=_("Name"), max_length=100, db_column="name", unique=True)

    class Meta:
        db_table = "country"
        verbose_name_plural = "Countries"

    def __str__(self):
        return str(self.id) + " - " + self.name


class State(CODEBaseModel):
    name = models.CharField(verbose_name=_("Name"), max_length=100, db_column="name")
    country = models.ForeignKey(
        Country,
        verbose_name=_("Country"),
        db_column="country",
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = "state"
        verbose_name_plural = "States"

    def __str__(self):
        return str(self.id) + " - " + self.name + ", " + self.country.name


class City(CODEBaseModel):
    name = models.CharField(verbose_name=_("Name"), max_length=100, db_column="name")
    state = models.ForeignKey(
        State,
        verbose_name=_("State"),
        db_column="state",
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = "city"
        verbose_name_plural = "Cities"

    def __str__(self):
        return str(self.id) + " - " + self.name + ", "+ self.state.name + ", " + self.state.country.name
