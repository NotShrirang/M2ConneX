from rest_framework.serializers import ModelSerializer, SerializerMethodField, ValidationError
from experience.models import Experience


class ExperienceSerializer(ModelSerializer):
    userName = SerializerMethodField()
    profilePicture = SerializerMethodField()

    class Meta:
        model = Experience
        fields = ['id', 'user', 'company', 'designation', 'description', 'startDate', 'endDate', 'isCurrent']
        read_only_fields = ['id', 'user']
        list_fields = ['id', 'user', 'company', 'designation', 'description', 'startDate', 'endDate', 'isCurrent']
        get_fields = ['id', 'user', 'company', 'designation', 'description', 'startDate', 'endDate', 'isCurrent']

    def get_userName(self, obj):
        return obj.user.firstName + " " + obj.user.lastName
    
    def get_profilePicture(self, obj):
        return obj.user.profilePicture if obj.user.profilePicture else None
    
    def validate(self, attrs):
        if attrs.get('endDate') and attrs.get('isCurrent'):
            raise ValidationError("Experience cannot be current and have an end date")
        if not attrs.get('endDate') and not attrs.get('isCurrent'):
            raise ValidationError("Experience must be current or have an end date")
        startDate = attrs.get('startDate')
        endDate = attrs.get('endDate')
        if endDate and startDate > endDate:
            raise ValidationError("Start date cannot be after end date")
        return attrs