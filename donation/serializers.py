from donation.models import Donation
from rest_framework.serializers import ModelSerializer, SerializerMethodField


class DonationSerializer(ModelSerializer):
    userName = SerializerMethodField()
    profilePicture = SerializerMethodField()

    class Meta:
        model = Donation
        fields = ['id', 'name', 'description', 'amount', 'department', 'userName', 'profilePicture']

    def get_userName(self, instance):
        return instance.user.name

    def get_profilePicture(self, instance):
        return instance.user.profilePicture
