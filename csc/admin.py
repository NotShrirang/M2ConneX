from django.contrib import admin
from csc.models import (
    City,
    State,
    Country
)

admin.site.register(City)
admin.site.register(State)
admin.site.register(Country)