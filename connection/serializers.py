from connection.models import (
   Connection
)
from rest_framework.serializers import ModelSerializer, SerializerMethodField


class ConnectionSerializer(ModelSerializer):
    userADetails = SerializerMethodField()
    userBDetails = SerializerMethodField()

    class Meta:
        model = Connection
        fields = ['id', 'userA', 'userB', 'status', 'createdAt', 'updatedAt', 'userADetails', 'userBDetails']
        list_fields = fields
        get_fields = fields

    def get_userADetails(self, obj):
        return {
            "firstName": obj.userA.firstName,
            "lastName": obj.userA.lastName,
            "profilePicture": obj.userA.profilePicture,
            "email": obj.userA.email,
            "department": obj.userA.department
        }

    def get_userBDetails(self, obj):
        return {
            "firstName": obj.userB.firstName,
            "lastName": obj.userB.lastName,
            "profilePicture": obj.userB.profilePicture,
            "email": obj.userB.email,
            "department": obj.userB.department
        }
