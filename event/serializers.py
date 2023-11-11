from event.models import Event
from rest_framework.serializers import ModelSerializer, SerializerMethodField


class EventSerializer(ModelSerializer):
    createdByUserName = SerializerMethodField()
    createdByUserProfilePicture = SerializerMethodField()

    class Meta:
        model = Event
        fields = ['id', 'name', 'description', 'date', 'time', 'venue', 'department', 'link', 'createdByUser', 'createdByUserName', 'createdByUserProfilePicture', 'createdAt', 'updatedAt']
        list_fields = fields
        get_fields = fields

        def getCreatedByUserName(self, obj):
            return obj.createdByUser.firstName + " " + obj.createdByUser.lastName
        
        def getCreatedByUserProfilePicture(self, obj):
            return obj.createdByUser.profilePicture
        

