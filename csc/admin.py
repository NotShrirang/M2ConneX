from django.contrib import admin
from csc.models import (
    City,
    State,
    Country
)

admin.site.register(Country)
admin.site.register(State)
admin.site.register(City)