from event.models import Event, EventImage
from rest_framework.serializers import ModelSerializer, SerializerMethodField


class EventSerializer(ModelSerializer):
    userName = SerializerMethodField()
    userProfilePicture = SerializerMethodField()
    images = SerializerMethodField()

    class Meta:
        model = Event
        fields = ['id', 'name', 'description', 'date', 'time', 'venue', 'department', 'link',
                  'createdByUser', 'userName', 'userProfilePicture', 'images', 'createdAt', 'updatedAt']
        list_fields = fields
        get_fields = fields

    def get_userName(self, obj):
        return obj.createdByUser.firstName + " " + obj.createdByUser.lastName

    def get_userProfilePicture(self, obj):
        return obj.createdByUser.profilePicture

    def get_images(self, obj):
        return EventImageSerializer(EventImage.objects.filter(event=obj), many=True).data


class EventImageSerializer(ModelSerializer):
    class Meta:
        model = EventImage
        fields = ['id', 'event', 'image']
        list_fields = fields
        get_fields = fields
