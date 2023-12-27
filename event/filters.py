import django_filters
from CODE.filters import CODEDateFilter
from .models import Event


class EventFilter(CODEDateFilter):
    name = django_filters.CharFilter(
        lookup_expr="istartswith", field_name="name")
    description = django_filters.CharFilter(
        lookup_expr="icontains", field_name="description")
    venue = django_filters.CharFilter(
        lookup_expr="icontains", field_name="venue")
    department = django_filters.CharFilter(
        lookup_expr="iexact", field_name="department")
    club = django_filters.CharFilter(
        lookup_expr="iexact", field_name="club__name")

    class Meta:
        model = Event
        fields = ['name', 'description', 'venue', 'department', 'club']
