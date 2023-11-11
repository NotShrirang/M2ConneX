from event.models import Event
from rest_framework.serializers import ModelSerializer


class EventSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'name', 'description', 'date', 'time', 'venue', 'department', 'link']
        list_fields = fields
        get_fields = fields
