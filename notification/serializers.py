from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'message', 'link',
                  'notificationType', 'user', 'isRead', 'createdAt', 'updatedAt']
        get_fields = fields
        list_fields = fields
