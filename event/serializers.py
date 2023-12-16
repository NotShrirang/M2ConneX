from event.models import Event, EventImage
from rest_framework.serializers import ModelSerializer, SerializerMethodField


class EventSerializer(ModelSerializer):
    userName = SerializerMethodField()
    userProfilePicture = SerializerMethodField()

    class Meta:
        model = Event
        fields = ['id', 'name', 'description', 'date', 'time', 'venue', 'department', 'link', 'createdByUser', 'userName', 'userProfilePicture', 'createdAt', 'updatedAt']
        list_fields = fields
        get_fields = fields

    def get_userName(self, obj):
        return obj.createdByUser.firstName + " " + obj.createdByUser.lastName

    def get_userProfilePicture(self, obj):
        return obj.createdByUser.profilePicture


class EventImageSerializer(ModelSerializer):
    eventName = SerializerMethodField()

    class Meta:
        model = EventImage
        fields = ['id', 'event', 'eventName', 'image']
        list_fields = fields
        get_fields = fields

        def get_EventName(self, obj):
            return obj.event.name
