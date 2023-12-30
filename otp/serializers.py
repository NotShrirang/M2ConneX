from rest_framework import serializers

from .models import OTP


class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = ['id', 'otp', 'user', 'createdAt', 'updatedAt']
        get_fields = fields
        list_fields = fields
