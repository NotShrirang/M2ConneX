from rest_framework.serializers import ModelSerializer, SerializerMethodField, ValidationError
from experience.models import Experience


class ExperienceSerializer(ModelSerializer):
    userName = SerializerMethodField()
    profilePicture = SerializerMethodField()

    class Meta:
        model = Experience
        fields = ['id', 'user', 'company', 'designation',
                  'description', 'startDate', 'endDate', 'isCurrent', 'userName', 'profilePicture']
        list_fields = fields
        get_fields = fields

    def get_userName(self, obj):
        return obj.user.firstName + " " + obj.user.lastName

    def get_profilePicture(self, obj):
        return obj.user.profilePicture if obj.user.profilePicture else None

    def validate(self, attrs):
        if 'endDate' not in attrs:
            if 'isCurrent' not in attrs:
                raise ValidationError(
                    "Experience must be current or have an end date")
            else:
                if attrs.get('isCurrent') is False:
                    raise ValidationError(
                        "Experience must be current or have an end date")
        startDate = attrs.get('startDate')
        endDate = attrs.get('endDate')
        if endDate and startDate > endDate:
            raise ValidationError("Start date cannot be after end date")
        return attrs
