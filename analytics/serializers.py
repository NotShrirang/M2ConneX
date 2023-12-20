from rest_framework import serializers
from .models import UserAnalytics
from connection.models import Connection
from django.db.models import Q


class UserAnalyticsSerializer(serializers.ModelSerializer):
    profileUserName = serializers.SerializerMethodField()
    visitorName = serializers.SerializerMethodField()
    isConnected = serializers.SerializerMethodField()

    class Meta:
        model = UserAnalytics
        fields = ['id', 'profileUser', 'profileUserName', 'visitor',
                  'visitorName', 'analyticsType', 'isConnected', 'createdAt', 'updatedAt']
        list_fields = fields
        get_fields = fields
        read_only_fields = ['id', 'createdAt', 'updatedAt']

    def get_profileUserName(self, obj):
        return f"{obj.profileUser.firstName} {obj.profileUser.lastName}"

    def get_visitorName(self, obj):
        return f"{obj.visitor.firstName} {obj.visitor.lastName}"

    def get_isConnected(self, obj):
        return Connection.objects.filter(
            Q(
                userA=obj.profileUser,
                userB=obj.visitor
            ) | Q(
                userA=obj.visitor,
                userB=obj.profileUser
            )
        ).exists()
