from donation.models import Donation
from rest_framework.serializers import ModelSerializer

class DonationSerializer(ModelSerializer):
    class Meta:
        model = Donation
        fields = '__all__'