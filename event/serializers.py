from event.models import Event, EventImage
from rest_framework.serializers import ModelSerializer, SerializerMethodField


class EventSerializer(ModelSerializer):
    userName = SerializerMethodField()
    profilePicture = SerializerMethodField()
    images = SerializerMethodField()
    clubName = SerializerMethodField()
    clubLogo = SerializerMethodField()

    class Meta:
        model = Event
        fields = ['id', 'name', 'description', 'date', 'time', 'venue',
                  'department', 'link', 'createdByUser', 'userName',
                  'profilePicture', 'images', 'isClubEvent', 'club',
                  'clubName', 'clubLogo', 'createdAt', 'updatedAt']
        list_fields = fields
        get_fields = fields

    def get_userName(self, obj):
        return obj.createdByUser.firstName + " " + obj.createdByUser.lastName

    def get_profilePicture(self, obj):
        return obj.createdByUser.profilePicture

    def get_images(self, obj):
        return EventImageSerializer(EventImage.objects.filter(event=obj),
                                    many=True).data

    def get_clubName(self, obj):
        if obj.isClubEvent:
            return obj.club.name
        return None

    def get_clubLogo(self, obj):
        if obj.isClubEvent:
            return obj.club.logo
        return None


class EventImageSerializer(ModelSerializer):
    class Meta:
        model = EventImage
        fields = ['id', 'event', 'image']
        list_fields = fields
        get_fields = fields
