from connection.models import (
    Connection
)
from rest_framework.serializers import ModelSerializer, SerializerMethodField, ValidationError
from users.models import (
    AlumniPortalUser
)
from django.db import models


class ConnectionSerializer(ModelSerializer):
    userADetails = SerializerMethodField()
    userBDetails = SerializerMethodField()
    mutualConnections = SerializerMethodField()

    class Meta:
        model = Connection
        fields = ['id', 'userA', 'userB', 'status', 'createdAt',
                  'updatedAt', 'userADetails', 'userBDetails',
                  'mutualConnections']
        list_fields = fields
        get_fields = fields
        unique_together = ('userA', 'userB')

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

    def get_mutualConnections(self, obj):
        userA_connections = Connection.objects.filter(
            (models.Q(userA=obj.userA) | models.Q(
                userB=obj.userA)) & models.Q(status='accepted')
        )
        userB_connections = Connection.objects.filter(
            (models.Q(userA=obj.userB) | models.Q(
                userB=obj.userB)) & models.Q(status='accepted')
        )
        mutual_connections = userA_connections.intersection(userB_connections)
        return mutual_connections.count()

    def validate(self, attrs):
        userA = AlumniPortalUser.objects.filter(id=attrs.get('userA').id)
        if not userA.exists():
            raise ValidationError("User A does not exist")
        userB = AlumniPortalUser.objects.filter(id=attrs.get('userB').id)
        if not userB.exists():
            raise ValidationError("User B does not exist")
        if userA == userB:
            raise ValidationError("User A and User B cannot be same")
        if Connection.objects.filter(userA=userA.first(), userB=userB.first()).exists():
            raise ValidationError("Connection already exists")
        if Connection.objects.filter(userA=userB.first(), userB=userA.first()).exists():
            raise ValidationError("Connection already exists")
        try:
            status = attrs.get('status')
        except Exception as e:
            attrs['status'] = 'pending'
        if status not in ['pending', 'accepted']:
            raise ValidationError("Invalid status")
        return super().validate(attrs)

    def create(self, validated_data: dict):
        try:
            status = validated_data.get('status')
        except Exception as e:
            print(e)
            status = 'pending'
        if status == 'accepted':
            validated_data['status'] = 'pending'
        return super().create(validated_data)
